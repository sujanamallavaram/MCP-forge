from fastapi import FastAPI
from pydantic import BaseModel
from backend.tool_generator import generate_tool
from backend.analyzers.java_analyzer import analyze_java_code
from backend.analyzers.python_analyzer import analyze_python_code
from backend.language_detector import detect_language


app = FastAPI(title="MCP Forge")


class CodeRequest(BaseModel):
    code: str
    language: str | None = None

@app.get("/")
def root():
    return {
        "message": "MCP Forge backend is running!"
    }


@app.post("/analyze")
def analyze_code(request: CodeRequest):
    language = request.language or detect_language(request.code)

    if language.lower() == "java":
        analysis = analyze_java_code(request.code)
    else:
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