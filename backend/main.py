from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


from backend.tool_generator import generate_tool
from backend.analyzers.java_analyzer import analyze_java_code
from backend.analyzers.python_analyzer import analyze_python_code
from backend.language_detector import detect_language
from backend.execution_service import ExecutionService
from backend.tool_registry import ToolRegistry
from backend.mcp_server import mcp_server, register_mcp_tool

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp_server.session_manager.run():
        yield
app = FastAPI(
    title="MCP Forge",
    lifespan=lifespan
)
app.mount(
    "/mcp",
    mcp_server.streamable_http_app(
        streamable_http_path="/",
        host="127.0.0.1"
    )
)
tool_registry = ToolRegistry()


class CodeRequest(BaseModel):
    code: str
    language: str | None = None


class ExecuteRequest(BaseModel):
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

    tools = []

    for function in analysis["functions"]:
        tool = generate_tool(function).model_dump()

        executable_function = None

        if language.lower() == "python":
            from backend.function_loader import load_functions

            loaded_functions = load_functions(request.code)
            executable_function = loaded_functions.get(function["name"])

        tool_registry.register(tool, executable_function)
        register_mcp_tool(tool, executable_function)
        tools.append(tool)

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

    function = tool_registry.get_function(request.tool_name)

    if function is None:
        raise HTTPException(
            status_code=404,
            detail=f"Tool '{request.tool_name}' is not registered."
        )

    try:
        result = service.execute_registered_function(
            function,
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