from fastapi import FastAPI
from pydantic import BaseModel
from backend.tool_generator import generate_tool

from backend.analyzers.python_analyzer import analyze_python_code


app = FastAPI(title="MCP Forge")


class CodeRequest(BaseModel):
    code: str


@app.get("/")
def root():
    return {
        "message": "MCP Forge backend is running!"
    }


@app.post("/analyze")
def analyze_code(request: CodeRequest):
    analysis = analyze_python_code(request.code)

    if not analysis["success"]:
        return analysis

    tools = [
        generate_tool(function).model_dump()
        for function in analysis["functions"]
    ]

    return {
        "analysis": analysis,
        "tools": tools
    }