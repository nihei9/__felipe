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
from . import config
from . import dot
from . import group
import docopt
import glob
import os

def main():
    args = docopt.docopt(__doc__, version = "1.0.0")

    config_file = args["--config"]
    src_dir = args["--src_dir"]
    out_dir = args["--out_dir"]

    conf = config.load(config_file)

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

def load_file(conf, filename, components):
    c = component.load(filename, conf)
    if c != None:
        components[c.component_id] = c
        return c
    
    g = group.load(filename, conf)
    if g != None:
        return g
