from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.tool_generator import generate_tool
from backend.analyzers.java_analyzer import analyze_java_code
from backend.analyzers.python_analyzer import analyze_python_code
from backend.language_detector import detect_language
from backend.execution_service import ExecutionService
from backend.tool_registry import ToolRegistry


app = FastAPI(title="MCP Forge")
tool_registry = ToolRegistry()

class CodeRequest(BaseModel):
    code: str
    language: str | None = None

class ExecuteRequest(BaseModel):
    code: str
    tool_name: str
    arguments: dict = {}

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

    for tool in tools:
        tool_registry.register(tool)

    return {
        "analysis": analysis,
        "tools": tools
    }

@app.get("/tools")
def list_tools():
    return {
        "tools": tool_registry.get_all()
    }

@app.post("/execute")
def execute_tool(request: ExecuteRequest):
    service = ExecutionService()

    try:
        service.load_code(request.code)

        result = service.execute(
            request.tool_name,
            request.arguments
        )

        return {
            "success": True,
            "tool": request.tool_name,
            "result": result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )