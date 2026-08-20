from typing import Any

from backend.mcp_schema import MCPTool


def python_type_to_json_type(python_type: str | None) -> str:
    """Convert common Python types to JSON Schema types."""

    type_mapping = {
        "str": "string",
        "int": "integer",
        "float": "number",
        "bool": "boolean",
        "list": "array",
        "dict": "object",
    }

    return type_mapping.get(python_type, "string")


def generate_tool(function: dict[str, Any]) -> MCPTool:
    """Convert analyzed function information into an MCPTool."""

    properties = {}
    required = []

    for parameter in function["parameters"]:
        name = parameter["name"]
        python_type = parameter["type"]

        # Ignore self when converting class methods
        if name == "self":
            continue

        properties[name] = {
            "type": python_type_to_json_type(python_type)
        }

        # Parameters without type hints are still treated as required.
        required.append(name)

    input_schema = {
        "type": "object",
        "properties": properties,
        "required": required,
    }

    description = (
        function["docstring"]
        or f"Execute the {function['name']} function."
    )

    return MCPTool(
        name=function["name"],
        description=description,
        input_schema=input_schema,
    )