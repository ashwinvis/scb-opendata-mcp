import asyncio
from .server import mcp


def main():
    # mcp.run()
    asyncio.run(mcp.run_async(transport="streamable-http", port=6767))


if __name__ == "__main__":
    main()
