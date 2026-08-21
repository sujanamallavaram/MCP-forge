# MCP Forge

AI-powered platform for converting source code into executable Model Context Protocol (MCP) tools.

## Overview

MCP Forge analyzes source code, identifies functions, generates tool definitions, registers them with an MCP server, and allows clients to execute the generated tools through the MCP protocol.

The project is designed to simplify the process of turning ordinary functions into reusable MCP-compatible tools.

## Features

- Source code analysis
- Python function analysis
- Java source analysis
- Automatic tool schema generation
- Dynamic function loading
- MCP tool registration
- Tool execution
- Input validation
- Security validation
- NVIDIA-powered AI services
- MCP JSON-RPC communication
- Support for dynamically generated tools

## Architecture

```text
Source Code
     |
     v
Language Detection
     |
     v
Code Analyzer
     |
     +---- Python Analyzer
     |
     +---- Java Analyzer
     |
     v
Tool Generator
     |
     v
Tool Registry
     |
     v
MCP Server
     |
     v
MCP Client
     |
     v
Tool Execution

Project Structure:
MCP-forge/
│
├── README.md
├── .gitignore
│
└── backend/
    │
    ├── analyzers/
    │   ├── java_analyzer.py
    │   └── python_analyzer.py
    │
    ├── execution_service.py
    ├── function_loader.py
    ├── language_detector.py
    ├── main.py
    ├── mcp_schema.py
    ├── mcp_server.py
    ├── nvidia_service.py
    ├── requirements.txt
    ├── security_validator.py
    ├── tool_executor.py
    ├── tool_generator.py
    └── tool_registry.py
MCP Workflow

MCP Forge follows this general workflow:

Accept source code.
Detect the programming language.
Analyze the source code.
Identify functions and their parameters.
Generate MCP-compatible tool definitions.
Load executable functions.
Register the tools with the MCP server.
Expose the tools through MCP.
Receive tool calls from an MCP client.
Validate and execute the requested function.
Return the result to the client.
Example

A Python function such as:

def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)

can be analyzed and represented as an MCP tool with an input schema similar to:

{
  "name": "factorial",
  "description": "Computes the factorial of integer n.",
  "input_schema": {
    "type": "object",
    "properties": {
      "n": {
        "type": "integer"
      }
    },
    "required": ["n"]
  }
}

The generated tool can then be registered with the MCP server and invoked through an MCP client.

Technologies
Python
FastAPI
Model Context Protocol (MCP)
Pydantic
NVIDIA AI services
JSON-RPC
Uvicorn
Running the Backend

Create and activate a virtual environment:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r backend/requirements.txt

Start the backend server:

uvicorn backend.main:app --reload

The server will be available locally through the configured FastAPI endpoint.

MCP Testing

MCP Forge can be tested using an MCP-compatible client or by sending JSON-RPC requests to the MCP endpoint.

The MCP workflow includes:

initialize
tools/list
tools/call

Example generated tools can include:

cube
power
factorial
Development Status

The core MCP tool generation and execution workflow has been implemented and tested with dynamically generated Python functions.

Future Improvements
Additional programming language support
Improved AI-based code generation
Persistent tool storage
Authentication and authorization
Tool versioning
Web-based management interface
Improved execution sandboxing
Automated test generation
Docker deployment
Production-ready MCP client integration
License

This project is currently under development.



### 2. Save it


Press:


**Ctrl + S**


### 3. Check the README


Run:


```powershell
Get-Content README.md