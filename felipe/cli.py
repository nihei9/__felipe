"""felipe

Usage:
    felipe [--config <CONFIG_FILE>] [--src_dir <SRC_DIR>] [--out_dir <OUT_DIR>]
    felipe -h | --help

Options:
    -c <CONFIG_FILE> --config=<CONFIG_FILE> Configuration file
                                            [default: ./config.yaml]
    -s <SRC_DIR> --src_dir=<SRC_DIR>        Source directory
                                            [default: ./]
    -o <OUT_DIR> --out_dir=<OUT_DIR>        Output directory
                                            [default: ./]
    -h --help                               help
"""

from . import component
from . import dot
from . import group
from . import relation
import copy
import docopt
import glob
import json
import os
import yaml

def main():
    args = docopt.docopt(__doc__, version = "1.0.0")

    config_file = args["--config"]
    src_dir = args["--src_dir"]
    out_dir = args["--out_dir"]

    conf = load_config(config_file)

    input_files = glob.glob(os.path.join(src_dir, "*.json"))
    components = {}
    for filename in input_files:
        f = load_file(conf, filename, components)
        if (f is None):
            continue
        
        basename = os.path.basename(filename)
        output_filename = os.path.join(out_dir, "%s.dot" % basename)
        if (f.kind == "component"):
            dot.write_component(conf, f, components, output_filename)
        elif (f.kind == "group"):
            dot.write_group(conf, f, components, output_filename)

class Config:
    def __init__(self):
        self.__components = {}
        self.__relations = {}
    
    def set_base_component(self, component):
        self.__base_component = component
    
    def append_component(self, component):
        self.__components[component.component_type] = copy.deepcopy(component)
    
    @property
    def base_component(self):
        return self.__base_component

    @property
    def components(self):
        return self.__components

    def set_base_relation(self, relation):
        self.__base_relation = relation
    
    def append_relation(self, relation):
        self.__relations[relation.relation_type] = copy.deepcopy(relation)
    
    @property
    def base_relation(self):
        return self.__base_relation

    @property
    def relations(self):
        return self.__relations

def load_config(filename):
    config = Config()

    with open(filename, mode = 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

        bc_data = data.get("base_component")
        if (bc_data != None):
            appearance = bc_data.get("appearance") or {}
            bc = component.Config("", "", [], [], appearance)
            config.set_base_component(bc)
        
        data.setdefault("components", {})
        cs_data = data.get("components")
        for ctype, attrs in cs_data.items():
            base = attrs.get("base")
            unique = attrs.get("unique_keys") or []
            label = attrs.get("label_keys") or []
            appearance = attrs.get("appearance") or {}
            c = component.Config(ctype, base, unique, label, appearance)
            config.append_component(c)

        br_data = data.get("base_relation")
        if (br_data != None):
            direction = br_data.get("direction") or ""
            appearance = br_data.get("appearance") or {}
            br = relation.Config("", "", direction, appearance)
            config.set_base_relation(br)
        
        data.setdefault("relations", {})
        rs_data = data.get("relations")
        for rtype, attrs in rs_data.items():
            base = attrs.get("base")
            direction = attrs.get("direction") or ""
            appearance = attrs.get("appearance") or {}
            r = relation.Config(rtype, base, direction, appearance)
            config.append_relation(r)
    
    complemented_config = Config()
    
    complemented_config.set_base_component(config.base_component)
    complemented_config.set_base_relation(config.base_relation)

    for c in config.components.values():
        cc = complement_component(c, config.components, config.base_component)
        complemented_config.append_component(cc)
    
    for c in config.relations.values():
        cc = complement_relation(c, config.relations, config.base_relation)
        complemented_config.append_relation(cc)
    
    return complemented_config

def complement_component(c, cs, default):
    """
    Complement a configuration of a component
    
    Parameters
    ----------
    c : ComponentConfig
        Configuration of a component
    cs : Dict of ComponentConfig (component_type -> ComponentConfig)
        Configurations of all components
    default : ComponentConfig
        Default configuration of a component
    
    Returns
    -------
    ComponentConfig
        Complemented configuration
    """

    cc = component.Config(c.component_type, c.base, default.unique_keys, default.label_keys, default.appearance)
    return complement_component_r(c, cs, cc, {})

def complement_component_r(c, cs, cc, marks):
    if (c.component_type in marks):
        # TODO ERROR
        return cc
    
    marks[c.component_type] = True

    new_cc = cc
    if (c.base):
        new_cc = complement_component_r(cs[c.base], cs, cc, marks)
    
    unique_keys = new_cc.unique_keys
    if (len(c.unique_keys) >= 1):
        unique_keys = c.unique_keys
    
    label_keys = new_cc.label_keys
    if (len(c.label_keys) >= 1):
        label_keys = c.label_keys
    
    appearance = new_cc.appearance
    for k, v in c.appearance.items():
        appearance[k] = v

    return component.Config(cc.component_type, cc.base, unique_keys, label_keys, appearance)

def complement_relation(c, cs, default):
    """
    Complement a configuration of a relation

    Parameters
    ----------
    c : RelationConfig
        Configuration of a relation
    cs : Dict of RelationConfig (relation_type -> RelationConfig)
        Configurations of all relations
    default : RelationConfig
        Default configuration of a relation
    
    Returns
    -------
    RelationConfig
        Complemented configuration
    """

    cc = relation.Config(c.relation_type, c.base, c.direction, default.appearance)
    return complement_relation_r(c, cs, cc, {})

def complement_relation_r(c, cs, cc, marks):
    if (c.relation_type in marks):
        # TODO ERROR
        return cc
    
    marks[c.relation_type] = True

    new_cc = cc
    if (c.base):
        new_cc = complement_relation_r(cs[c.base], cs, cc, marks)
    
    appearance = new_cc.appearance
    for k, v in c.appearance.items():
        appearance[k] = v

    return relation.Config(cc.relation_type, cc.base, cc.direction, appearance)

def load_file(conf, filename, components):
    with open(filename, mode = 'r') as f:
        data = json.load(f)
        kind = data.get("kind")
        if (kind == "component"):
            c = load_component(conf, data)
            components[c.component_id] = c
            return c
        if (kind == "group"):
            return load_group(conf, data)

def load_component(conf, data):
    c = component.Component(conf.components[data["component"]["type"]], data["component"])
    
    for ddata in data["dependencies"]:
        dc = component.Component(conf.components[ddata["type"]], ddata)
        
        for rdata in ddata["relations"]:
            r = relation.Relation(conf.relations[rdata["type"]], rdata)
            c.relate_to(dc, r)
    
    return c

def load_group(conf, data):
    g = group.Group()

    for cdata in data["group"]["components"]:
        c = component.Component(conf.components[cdata["type"]], cdata)
        g.append(c)
    
    return g
