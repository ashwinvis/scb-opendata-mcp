import asyncio
from .server import mcp


def main():
    # mcp.run()
    # asyncio.run(mcp.run_async(transport="http", host="127.0.0.1", port=6767))
    mcp.run(transport="http", host="0.0.0.0", port=6767)


if __name__ == "__main__":
    main()
