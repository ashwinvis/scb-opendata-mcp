# import asyncio
from typing import Literal
from cyclopts import App
from .server import mcp

app = App()


@app.default
def main(
    transport: Literal["stdio", "http"] = "http",
    host: str = "0.0.0.0",
    port: int = 6767,
):
    if transport == "http":
        mcp.run(transport="http", host=host, port=port)
    else:
        mcp.run(transport="stdio", show_banner=False)
    # asyncio.run(mcp.run_async(transport="http", host="127.0.0.1", port=6767))


if __name__ == "__main__":
    main()
