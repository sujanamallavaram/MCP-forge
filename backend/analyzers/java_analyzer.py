import re


def analyze_java_code(code: str) -> dict:
    """Analyze basic Java methods and return MCP-friendly metadata."""

    functions = []

    method_pattern = re.compile(
        r"""
        (?P<visibility>public|private|protected)?\s*
        (?P<static>static\s+)?
        (?P<return_type>[\w<>\[\], ?]+)\s+
        (?P<name>\w+)\s*
        \(
            (?P<parameters>[^)]*)
        \)\s*
        \{
        """,
        re.VERBOSE,
    )

    for match in method_pattern.finditer(code):
        name = match.group("name")
        return_type = match.group("return_type").strip()
        parameters_text = match.group("parameters").strip()

        parameters = []

        if parameters_text:
            for parameter in parameters_text.split(","):
                parameter = parameter.strip()

                parts = parameter.split()

                if len(parts) >= 2:
                    parameter_type = " ".join(parts[:-1])
                    parameter_name = parts[-1]

                    parameters.append(
                        {
                            "name": parameter_name,
                            "type": parameter_type,
                        }
                    )

        functions.append(
            {
                "name": name,
                "parameters": parameters,
                "return_type": return_type,
                "docstring": "",
                "is_async": False,
            }
        )

    return {
        "success": True,
        "imports": [],
        "functions": functions,
        "classes": [],
    }