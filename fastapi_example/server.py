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

# Create MCP sub-apps first
echo_app = echo_mcp.streamable_http_app()
math_app = math_mcp.streamable_http_app()

# Add middleware directly to sub-apps
echo_app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

math_app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

# Mount them
app.mount("/echo", echo_app)
app.mount("/math", math_app)

PORT = int(os.environ.get("PORT", 10000))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=PORT,
        proxy_headers=True,
        forwarded_allow_ips="*"
    )