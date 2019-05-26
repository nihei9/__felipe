import textwrap

def write_component(conf, component, components, output_filename):
    with open(output_filename, mode = 'w') as f:
        f.write("digraph G {\n")
        f.write("    rankdir=LR\n")
        f.write("    fontsize=11.0\n")
        
        f.write(gen_node_statement(conf, component, 1))

        for d in component.dependencies:
            f.write(gen_node_statement(conf, d, 1))
        
        for d_component_id, rs in component.relations.items():
            for r in rs:
                f.write(gen_edge_statement(conf, component.component_id, d_component_id, r, 1))
            
        f.write("}\n")

def write_group(conf, group, components, output_filename):
    with open(output_filename, mode = 'w') as f:
        f.write("digraph G {\n")
        f.write("    rankdir=LR\n")
        f.write("    fontsize=11.0\n")
        
        for component in group.components.values():
            c = components[component.component_id]

            f.write(gen_node_statement(conf, c, 1))

            for d in c.dependencies:
                f.write(gen_node_statement(conf, d, 1))

            for d_component_id, rs in c.relations.items():
                for r in rs:
                    f.write(gen_edge_statement(conf, c.component_id, d_component_id, r, 1))
            
        f.write("}\n")

def gen_node_statement(conf, component, depth):
    """
    Generates a node statement like `n1 [label = "Node #1"];`.

    Parameters
    ----------
    component : Component
        Component
    conf : ComponentConfig
        Component configuration
    depth : int
        Indent level
    
    Returns
    -------
    string
        A generated node statement.
    """

    if (depth < 0):
        depth = 0
    
    stmt_tmpl = "\"%s\" %s;\n"
    attrs = format_attrs(component.label, conf.components[component.component_type].appearance)
    stmt = stmt_tmpl % (component.component_id, attrs)
    return textwrap.indent(stmt, "    " * depth)

def gen_edge_statement(conf, component_id, d_component_id, relation, depth):
    if (depth < 0):
        depth = 0
    
    stmt_tmpl = "\"%s\" -> \"%s\" %s;\n"
    rconf = conf.relations[relation.relation_type]
    attrs = format_attrs("", rconf.appearance)
    stmt = ""
    if (rconf.direction == "<-"):
        stmt = stmt_tmpl % (d_component_id, component_id, attrs)
    elif (rconf.direction == "->"):
        stmt = stmt_tmpl % (component_id, d_component_id, attrs)
    else:
        stmt = stmt_tmpl % (d_component_id, component_id, attrs)
    
    return textwrap.indent(stmt, "    " * depth)

def format_attrs(label, attrs):
    s = ""
    for k, v in attrs.items():
        if (k == "label"):
            continue
        
        if (s != ""):
            s += " "
        s += f'{k} = {v}'
    
    if (s != ""):
        s += " "
    s += f'label = "{label}"'
    
    return f'[{s}]'
