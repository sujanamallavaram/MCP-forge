import ast
from types import ModuleType


def load_functions(code: str) -> dict[str, object]:
    """
    Load function definitions from Python source code.

    This is a prototype loader. It only accepts Python code that
    successfully parses and extracts top-level function definitions.
    """

    tree = ast.parse(code)

    function_names = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    namespace: dict[str, object] = {}

    compiled = compile(tree, "<mcpforge>", "exec")

    exec(compiled, {"__builtins__": {}}, namespace)

    return {
        name: namespace[name]
        for name in function_names
        if name in namespace
    }