import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not NVIDIA_API_KEY:
    raise RuntimeError("NVIDIA_API_KEY is not set.")


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY,
    timeout=15.0,
    max_retries=0,
)


def ask_nvidia(prompt: str) -> str:
    """Send a prompt to NVIDIA Nemotron and return the response."""

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=2048,
    )

    return response.choices[0].message.content


def generate_tool_description(function: dict) -> str:
    """Generate a concise MCP tool description using NVIDIA."""

    prompt = f"""
You are helping MCP Forge convert Python functions into MCP tools.

Analyze this function metadata:

Function name: {function["name"]}
Parameters: {function["parameters"]}
Return type: {function["return_type"]}
Docstring: {function["docstring"]}

Write a concise, developer-friendly description of what this tool does.

Rules:
- Return only the description.
- Do not use markdown.
- Do not invent behavior that is not supported by the metadata.
- Keep it under 30 words.
"""

    try:
        return ask_nvidia(prompt).strip()

    except Exception as error:
        print(f"NVIDIA unavailable, using fallback description: {error}")

        docstring = (function.get("docstring") or "").strip()

        if docstring:
            return docstring

        name = function["name"].replace("_", " ")

        return f"Executes the {name} function."