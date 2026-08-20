from typing import Any


class ToolRegistry:
    """Store and retrieve generated MCP tools."""

    def __init__(self):
        self.tools: dict[str, dict[str, Any]] = {}

    def register(self, tool: dict[str, Any]):
        """Register a generated tool."""
        self.tools[tool["name"]] = tool

    def get(self, name: str) -> dict[str, Any] | None:
        """Get a tool by name."""
        return self.tools.get(name)

    def get_all(self) -> list[dict[str, Any]]:
        """Return all registered tools."""
        return list(self.tools.values())

    def clear(self):
        """Remove all registered tools."""
        self.tools.clear()