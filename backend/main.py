from fastapi import FastAPI

app = FastAPI(title="MCP Forge")


@app.get("/")
def root():
    return {
        "message": "MCP Forge backend is running!"
    }