from fastapi import FastAPI
from fastapi_example.math_server import mcp as math_mcp
from fastapi_example.echo_server import mcp as echo_mcp

app = FastAPI()

app.mount("/math", math_mcp.streamable_http_app())
app.mount("/echo", echo_mcp.streamable_http_app())

@app.get("/")
def root():
    return {"status": "running"}