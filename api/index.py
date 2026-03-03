import contextlib
from fastapi import FastAPI
from fastapi_example.math_server import mcp as math_mcp
from fastapi_example.echo_server import mcp as echo_mcp

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(math_mcp.session_manager.run())
        await stack.enter_async_context(echo_mcp.session_manager.run())
        yield

app = FastAPI(lifespan=lifespan)

app.mount("/math", math_mcp.streamable_http_app())
app.mount("/echo", echo_mcp.streamable_http_app())

@app.get("/")
def root():
    return {"status": "running"}