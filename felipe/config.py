import copy
import yaml

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

class ComponentConfig:
    def __init__(self, ctype, base, unique_keys, label_keys, appearance):
        self.__type = ctype
        self.__base = base
        self.__unique_keys = unique_keys
        self.__label_keys = label_keys
        self.__appearance = appearance
    
    @property
    def component_type(self):
        return self.__type
    
    @property
    def base(self):
        return self.__base
    
    @property
    def unique_keys(self):
        return self.__unique_keys
    
    @property
    def label_keys(self):
        return self.__label_keys
    
    @property
    def appearance(self):
        return self.__appearance

class RelationConfig:
    def __init__(self, rtype, base, direction, appearance):
        self.__type = rtype
        self.__base = base
        self.__direction = direction
        self.__appearance = appearance
    
    @property
    def relation_type(self):
        return self.__type
    
    @property
    def base(self):
        return self.__base
    
    @property
    def direction(self):
        return self.__direction
    
    @property
    def appearance(self):
        return self.__appearance

def load(filename):
    config = Config()

    with open(filename, mode = 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

        bc_data = data.get("base_component")
        if (bc_data != None):
            appearance = bc_data.get("appearance") or {}
            bc = ComponentConfig("", "", [], [], appearance)
            config.set_base_component(bc)
        
        data.setdefault("components", {})
        cs_data = data.get("components")
        for ctype, attrs in cs_data.items():
            base = attrs.get("base")
            unique = attrs.get("unique_keys") or []
            label = attrs.get("label_keys") or []
            appearance = attrs.get("appearance") or {}
            c = ComponentConfig(ctype, base, unique, label, appearance)
            config.append_component(c)

        br_data = data.get("base_relation")
        if (br_data != None):
            direction = br_data.get("direction") or ""
            appearance = br_data.get("appearance") or {}
            br = RelationConfig("", "", direction, appearance)
            config.set_base_relation(br)
        
        data.setdefault("relations", {})
        rs_data = data.get("relations")
        for rtype, attrs in rs_data.items():
            base = attrs.get("base")
            direction = attrs.get("direction") or ""
            appearance = attrs.get("appearance") or {}
            r = RelationConfig(rtype, base, direction, appearance)
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

    cc = ComponentConfig(c.component_type, c.base, default.unique_keys, default.label_keys, default.appearance)
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

    return ComponentConfig(cc.component_type, cc.base, unique_keys, label_keys, appearance)

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

    cc = RelationConfig(c.relation_type, c.base, c.direction, default.appearance)
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

    return RelationConfig(cc.relation_type, cc.base, cc.direction, appearance)
