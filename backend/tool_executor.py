from typing import Any, Callable


class ToolExecutor:
    """Execute generated MCP tools safely."""

    def __init__(self):
        self.tools: dict[str, Callable] = {}

    def register_tool(self, name: str, function: Callable):
        """Register a function as an executable tool."""
        self.tools[name] = function

    def execute(self, name: str, arguments: dict[str, Any]) -> Any:
        """Execute a registered tool with the supplied arguments."""

        if name not in self.tools:
            raise ValueError(f"Tool '{name}' is not registered.")

        function = self.tools[name]

        try:
            return function(**arguments)
        except TypeError as error:
            raise ValueError(
                f"Invalid arguments for tool '{name}': {error}"
            ) from error
        except Exception as error:
            raise RuntimeError(
                f"Tool '{name}' failed during execution: {error}"
            ) from error