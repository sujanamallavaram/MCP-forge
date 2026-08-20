import ast


BLOCKED_NAMES = {
    "eval",
    "exec",
    "compile",
    "__import__",
    "open",
    "input",
}


BLOCKED_ATTRIBUTES = {
    "system",
    "popen",
    "remove",
    "unlink",
    "rmdir",
    "rmtree",
}


def validate_python_code(code: str) -> tuple[bool, list[str]]:
    """
    Perform a basic security check on Python source code.

    Returns:
        (True, []) when the code passes validation.
        (False, reasons) when dangerous constructs are detected.
    """

    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return False, [f"Syntax error: {error}"]

    issues = []

    for node in ast.walk(tree):

        # Block dangerous built-in function calls.
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in BLOCKED_NAMES:
                    issues.append(
                        f"Blocked function call: {node.func.id}"
                    )

            elif isinstance(node.func, ast.Attribute):
                if node.func.attr in BLOCKED_ATTRIBUTES:
                    issues.append(
                        f"Blocked attribute call: {node.func.attr}"
                    )

        # Block direct imports of suspicious modules.
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split(".")[0]

                if module in {
                    "os",
                    "subprocess",
                    "shutil",
                    "socket",
                    "sys",
                }:
                    issues.append(
                        f"Blocked import: {module}"
                    )

        if isinstance(node, ast.ImportFrom):
            module = (node.module or "").split(".")[0]

            if module in {
                "os",
                "subprocess",
                "shutil",
                "socket",
                "sys",
            }:
                issues.append(
                    f"Blocked import: {module}"
                )

    return len(issues) == 0, issues