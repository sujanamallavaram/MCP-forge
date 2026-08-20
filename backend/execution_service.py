from typing import Any

from backend.function_loader import load_functions
from backend.security_validator import validate_python_code
from backend.tool_executor import ToolExecutor


class ExecutionService:
    """Validate, load, and execute Python tools."""

    def __init__(self):
        self.executor = ToolExecutor()

    def load_code(self, code: str):
        """Validate and load functions from Python source code."""

        is_safe, issues = validate_python_code(code)

        if not is_safe:
            raise ValueError(
                "Code failed security validation: " + "; ".join(issues)
            )

        functions = load_functions(code)

        for name, function in functions.items():
            self.executor.register_tool(name, function)

    def execute(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Execute a loaded tool."""

        return self.executor.execute(tool_name, arguments)