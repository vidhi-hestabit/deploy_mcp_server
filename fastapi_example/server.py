import contextlib
import os
from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware
from echo_server import mcp as echo_mcp
from math_server import mcp as math_mcp


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(echo_mcp.session_manager.run())
        await stack.enter_async_context(math_mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)

# Allow Render domain
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # or restrict to your render domain
)

app.mount("/echo", echo_mcp.streamable_http_app())
app.mount("/math", math_mcp.streamable_http_app())

PORT = int(os.environ.get("PORT", 10000))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)