import uuid
import subprocess


def generate_dot_for_ast(ast, filename="ast_graph"):
    """Generate a GraphViz DOT file for visualizing the AST."""
    if not ast:
        return (
            'digraph AST {\n    node [shape=box];\n    "root" [label="Empty AST"];\n}\n'
        )

    # Use a more visually appealing style
    dot_content = """digraph AST {
    // Graph styling
    graph [rankdir=TB, fontname="Arial", splines=true, overlap=false, nodesep=0.8];
    // Node styling
    node [fontname="Arial", style="filled", fillcolor="#f5f5f5", color="#333333", shape=box, fontsize=12];
    // Edge styling
    edge [color="#666666", arrowsize=0.8];
    
"""

    node_counter = 0
    node_ids = {}

    # Color palette for different node types
    node_colors = {
        "Program": "#e6f3ff",
        "Assignment": "#fff0e6",
        "BinaryOp": "#e6ffe6",
        "UnaryOp": "#e6ffff",
        "Literal": "#f2e6ff",
        "Identifier": "#ffe6e6",
        "FunctionCall": "#ffe6f2",
        "FunctionDef": "#e6f2ff",
        "IfStatement": "#fff2e6",
        "WhileLoop": "#f2ffe6",
        "ForLoop": "#ffe6ff",
        "Block": "#e6ffff",
        "ReturnStatement": "#ffffe6",
    }

    # Default color for unspecified node types
    default_color = "#f5f5f5"

    def get_node_id(node):
        nonlocal node_counter
        if id(node) not in node_ids:
            node_ids[id(node)] = f"node{node_counter}"
            node_counter += 1
        return node_ids[id(node)]

    def add_node(node, label, node_type=None):
        node_id = get_node_id(node)
        escaped_label = label.replace('"', '\\"')

        # Choose color based on node type
        fillcolor = (
            node_colors.get(node_type, default_color) if node_type else default_color
        )

        dot_content = (
            f'    "{node_id}" [label="{escaped_label}", fillcolor="{fillcolor}"];\n'
        )
        return dot_content

    def add_edge(parent, child, label=None):
        if child is None:
            return ""
        parent_id = get_node_id(parent)
        child_id = get_node_id(child)

        if label:
            return f'    "{parent_id}" -> "{child_id}" [label="{label}"];\n'
        else:
            return f'    "{parent_id}" -> "{child_id}";\n'

    def process_node(node):
        nonlocal dot_content

        if node is None:
            return

        # Get the node type for styling
        if hasattr(node, "__class__"):
            node_type = node.__class__.__name__
        else:
            node_type = str(type(node))

        if hasattr(node, "__dict__"):
            # For objects with attributes
            attribs = []
            for attr_name, attr_value in node.__dict__.items():
                # Skip attributes that are objects or lists we'll process separately
                if isinstance(
                    attr_value, (str, int, float, bool)
                ) and not attr_name.startswith("_"):
                    # Format the attribute nicely
                    if isinstance(attr_value, str):
                        # Truncate long strings
                        if len(attr_value) > 20:
                            attr_value = attr_value[:17] + "..."
                    attribs.append(f"{attr_name}: {attr_value}")

            # Create the node label with type and attributes
            label = f"{node_type}\\n{', '.join(attribs)}" if attribs else node_type
            dot_content += add_node(node, label, node_type)

            # Process children based on node type
            if node_type == "Program":
                if hasattr(node, "statements") and node.statements:
                    for i, stmt in enumerate(node.statements):
                        dot_content += add_edge(node, stmt, f"stmt_{i}")
                        process_node(stmt)

            elif node_type == "BinaryOp":
                if hasattr(node, "left"):
                    dot_content += add_edge(node, node.left, "left")
                    process_node(node.left)
                if hasattr(node, "right"):
                    dot_content += add_edge(node, node.right, "right")
                    process_node(node.right)

            elif node_type == "RangeOp":
                if hasattr(node, "start"):
                    dot_content += add_edge(node, node.start, "start")
                    process_node(node.start)
                if hasattr(node, "end"):
                    dot_content += add_edge(node, node.end, "end")
                    process_node(node.end)

            elif node_type == "UnaryOp":
                if hasattr(node, "expr"):
                    dot_content += add_edge(node, node.expr, "expr")
                    process_node(node.expr)

            elif node_type == "Assignment":
                if hasattr(node, "id"):
                    dot_content += add_edge(node, node.id, "id")
                    process_node(node.id)
                if hasattr(node, "expr"):
                    dot_content += add_edge(node, node.expr, "value")
                    process_node(node.expr)

            elif node_type == "FunctionCall":
                if hasattr(node, "args") and node.args:
                    for i, arg in enumerate(node.args):
                        dot_content += add_edge(node, arg, f"arg_{i}")
                        process_node(arg)

            elif node_type == "FunctionDef":
                if hasattr(node, "params") and node.params:
                    for i, param in enumerate(node.params):
                        dot_content += add_edge(node, param, f"param_{i}")
                        process_node(param)
                if hasattr(node, "body"):
                    dot_content += add_edge(node, node.body, "body")
                    process_node(node.body)

            elif node_type == "IfStatement":
                if hasattr(node, "condition"):
                    dot_content += add_edge(node, node.condition, "condition")
                    process_node(node.condition)
                if hasattr(node, "true_block"):
                    dot_content += add_edge(node, node.true_block, "then")
                    process_node(node.true_block)
                if hasattr(node, "else_block") and node.else_block:
                    dot_content += add_edge(node, node.else_block, "else")
                    process_node(node.else_block)

            elif node_type in ["WhileLoop", "ForLoop"]:
                if hasattr(node, "condition"):
                    dot_content += add_edge(node, node.condition, "condition")
                    process_node(node.condition)
                if hasattr(node, "iterator"):
                    dot_content += add_edge(node, node.iterator, "iterator")
                    process_node(node.iterator)
                if hasattr(node, "var"):
                    dot_content += add_edge(node, node.var, "var")
                    process_node(node.var)
                if hasattr(node, "block"):
                    dot_content += add_edge(node, node.block, "body")
                    process_node(node.block)

            elif node_type == "Block":
                if hasattr(node, "statements") and node.statements:
                    for i, stmt in enumerate(node.statements):
                        dot_content += add_edge(node, stmt, f"stmt_{i}")
                        process_node(stmt)

            elif node_type == "ReturnStatement":
                if hasattr(node, "expr"):
                    dot_content += add_edge(node, node.expr, "value")
                    process_node(node.expr)

            # Process any other attributes not covered above
            else:
                for attr_name, attr_value in node.__dict__.items():
                    if attr_name.startswith("_"):
                        continue

                    if isinstance(attr_value, list):
                        for i, item in enumerate(attr_value):
                            if item is not None:
                                dot_content += add_edge(node, item, f"{attr_name}_{i}")
                                process_node(item)
                    elif attr_value is not None and not isinstance(
                        attr_value, (str, int, float, bool)
                    ):
                        dot_content += add_edge(node, attr_value, attr_name)
                        process_node(attr_value)

        elif isinstance(node, list):
            # For lists (e.g., statement lists)
            list_node_id = f"list_{str(uuid.uuid4())[:8]}"
            temp_node = {"id": list_node_id, "type": "list"}
            node_ids[id(node)] = get_node_id(temp_node)
            dot_content += add_node(temp_node, "List", "List")

            for i, item in enumerate(node):
                if item is not None:
                    dot_content += add_edge(temp_node, item, f"item_{i}")
                    process_node(item)

    # Start processing from the root
    process_node(ast)
    dot_content += "}\n"

    # Write to file
    with open(f"{filename}.dot", "w") as f:
        f.write(dot_content)

    print(f"DOT file generated as {filename}.dot")

    # Auto-generate PNG using Graphviz
    try:
        subprocess.run(
            ["dot", "-Tpng", f"{filename}.dot", "-o", f"{filename}.png"], check=True
        )
        print(f"PNG image generated as {filename}.png")
    except FileNotFoundError:
        print(
            "Error: Graphviz 'dot' command not found. Install Graphviz to generate images."
        )
    except subprocess.CalledProcessError as e:
        print(f"Error generating PNG: {e}")

    return dot_content
