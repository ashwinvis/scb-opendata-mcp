"""
Integration test for FastMCP client with SCB server.

This test verifies that the FastMCP client can properly interact with
the SCB server implementation.
"""

import pytest
import pytest_asyncio
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport

from scb_opendata_mcp.server import mcp


@pytest_asyncio.fixture
async def main_mcp_client():
    """Fixture that provides a FastMCP client connected to the SCB server."""
    async with Client(transport=mcp) as mcp_client:
        yield mcp_client


@pytest.mark.asyncio
async def test_list_tools(main_mcp_client: Client[FastMCPTransport]):
    """Test that the client can list all available tools from the server."""
    list_tools = await main_mcp_client.list_tools()
    
    # The server should have multiple tools registered
    assert len(list_tools) == 13


@pytest.mark.asyncio
async def test_tool_execution(main_mcp_client: Client[FastMCPTransport]):
    """Test that a specific tool can be executed through the client."""
    # Test list_tables tool
    result = await main_mcp_client.call_tool(
        name="list_tables",
        arguments={}
    )
    
    # The result is a CallToolResult object, access the content
    import json
    # result.content is a list of TextContent objects
    content_json = result.content[0].text
    content = json.loads(content_json)
    
    # Should return a valid response structure
    assert "tables" in content
    assert isinstance(content["tables"], list)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
