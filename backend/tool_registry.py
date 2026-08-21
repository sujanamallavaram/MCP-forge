from typing import Any, Callable


class ToolRegistry:
    """Store generated MCP tools and their executable functions."""

    def __init__(self):
        self.tools: dict[str, dict[str, Any]] = {}
        self.functions: dict[str, Callable] = {}

    def register(
        self,
        tool: dict[str, Any],
        function: Callable | None = None,
    ):
        """Register tool metadata and its executable function."""

        name = tool["name"]

        self.tools[name] = tool

        if function is not None:
            self.functions[name] = function

    def get(self, name: str) -> dict[str, Any] | None:
        """Get tool metadata by name."""

        return self.tools.get(name)

    def get_function(self, name: str) -> Callable | None:
        """Get the executable function for a tool."""

        return self.functions.get(name)

    def get_all(self) -> list[dict[str, Any]]:
        """Return all registered tool metadata."""

        return list(self.tools.values())

    def clear(self):
        """Remove all registered tools and functions."""

        self.tools.clear()
        self.functions.clear()