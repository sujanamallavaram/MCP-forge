from mcp.server import MCPServer


mcp_server = MCPServer(
    name="MCP Forge",
    description="AI-powered tool generation and execution server.",
    version="1.0.0",
)


def register_mcp_tool(tool: dict, function):
    """Register one executable tool with the MCP server."""

    if function is None:
        return

    mcp_server.add_tool(
        function,
        name=tool["name"],
        description=tool.get("description", ""),
    )