import ast


def analyze_python_code(code: str) -> dict:
    """
    Analyze Python source code using the Abstract Syntax Tree (AST).
    Extract imports, functions, and classes.
    """

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {
            "success": False,
            "error": f"Invalid Python syntax: {e}"
        }

    imports = []
    functions = []
    classes = []

    # Analyze top-level and nested nodes
    for node in ast.walk(tree):

        # -------------------------
        # Imports
        # -------------------------
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    "name": alias.name,
                    "alias": alias.asname
                })

        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.append({
                    "name": f"{node.module}.{alias.name}",
                    "alias": alias.asname
                })

        # -------------------------
        # Functions
        # -------------------------
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            parameters = []

            for arg in node.args.args:
                parameters.append({
                    "name": arg.arg,
                    "type": (
                        ast.unparse(arg.annotation)
                        if arg.annotation
                        else None
                    )
                })

            functions.append({
                "name": node.name,
                "parameters": parameters,
                "return_type": (
                    ast.unparse(node.returns)
                    if node.returns
                    else None
                ),
                "docstring": ast.get_docstring(node),
                "is_async": isinstance(node, ast.AsyncFunctionDef)
            })

        # -------------------------
        # Classes
        # -------------------------
        elif isinstance(node, ast.ClassDef):
            methods = []

            for child in node.body:
                if isinstance(
                    child,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    methods.append(child.name)

            classes.append({
                "name": node.name,
                "methods": methods
            })

    return {
        "success": True,
        "imports": imports,
        "functions": functions,
        "classes": classes
    }