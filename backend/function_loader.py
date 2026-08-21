import ast


def load_functions(code: str) -> dict[str, object]:
    """
    Load function definitions from Python source code.

    This loader only accepts top-level Python function definitions
    and executes them with a restricted set of safe built-ins.
    """

    tree = ast.parse(code)

    function_names = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    namespace: dict[str, object] = {}

    safe_globals = {
        "__builtins__": {},

        # Safe type names needed for annotations
        "int": int,
        "str": str,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
        "tuple": tuple,
        "set": set,
    }

    compiled = compile(tree, "<mcpforge>", "exec")

    exec(compiled, safe_globals, namespace)

    # Make loaded functions available to each other.
    # This supports recursive functions while keeping the
    # restricted safe_globals namespace.
    for name in function_names:
        if name in namespace:
            safe_globals[name] = namespace[name]

    return {
        name: namespace[name]
        for name in function_names
        if name in namespace}