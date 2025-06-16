def generate_dot(node, dot_file):
    """
    Generates a .dot file from an AST for visualization, with color-coded nodes.
    """

    color_map = {
        "program": "gray",
        "statement_list": "whitesmoke",
        "assign": "lightblue",
        "if_statement": "lightcoral",
        "elseif": "lightsalmon",
        "else": "lightpink",
        "while_loop": "lightseagreen",
        "function_def": "mediumpurple",
        "param_list": "plum",
        "bin_op": "palegreen",
        "unary_op": "mediumaquamarine",
        "identifier": "khaki",
        "integer": "gold",
        "float": "goldenrod",
        "string": "orange",
        "expression_statement": "azure",
    }

    count = 0

    def get_id(n):
        nonlocal count
        if not hasattr(n, "id"):
            n.id = count
            count += 1
        return n.id

    def traverse(n):
        if n is None:
            return

        node_id = get_id(n)
        label = str(n.type)
        if n.leaf is not None:
            leaf_str = str(n.leaf).replace("\\", "\\\\").replace('"', '\\"')
            label += f"\\n{leaf_str}"

        color = color_map.get(n.type, "lightgrey")

        dot_file.write(f'  {node_id} [label="{label}", fillcolor="{color}"];\n')

        for child in n.children:
            child_id = get_id(child)
            dot_file.write(f"  {node_id} -> {child_id};\n")
            traverse(child)

    dot_file.write("digraph AST {\n")

    dot_file.write('  node [shape=box, style="rounded,filled"];\n')
    traverse(node)
    dot_file.write("}\n")
