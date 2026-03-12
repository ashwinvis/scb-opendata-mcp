"""
Test file for SCB FastMCP server.

This file contains basic tests to verify the server implementation.
Tests use mock responses to avoid hitting the actual API during testing.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
import json
from scb_opendata_mcp.server import (
    list_tables,
    get_table_info,
    search_tables,
    get_table_data,
    get_table_metadata,
    get_default_selection,
    list_codelists,
    get_codelist,
    get_codelist_metadata,
    list_saved_queries,
    get_saved_query,
    save_query,
    delete_saved_query,
    SCBAPIError,
    RateLimitError
)


@pytest.mark.asyncio
async def test_list_tables():
    """Test list_tables function"""
    mock_response = {
        "tables": [
            {"id": "BE0101A", "label": "Population by age and sex"}
        ],
        "page": 1,
        "totalPages": 1,
        "totalHits": 1,
        "links": []
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await list_tables()
        assert result["tables"][0]["id"] == "BE0101A"
        assert result["totalHits"] == 1


@pytest.mark.asyncio
async def test_list_tables_with_query():
    """Test list_tables with search query"""
    mock_response = {
        "tables": [
            {"id": "BE0101A", "label": "Employment statistics"}
        ],
        "page": 1,
        "totalPages": 1,
        "totalHits": 1,
        "links": []
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await list_tables(query="employment")
        assert result["tables"][0]["label"] == "Employment statistics"


@pytest.mark.asyncio
async def test_get_table_info():
    """Test get_table_info function"""
    mock_response = {
        "id": "BE0101A",
        "label": "Population by age and sex",
        "description": "Population statistics",
        "variables": [{"id": "Age", "label": "Age"}]
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await get_table_info("BE0101A")
        assert result["id"] == "BE0101A"
        assert result["label"] == "Population by age and sex"


@pytest.mark.asyncio
async def test_search_tables():
    """Test search_tables function"""
    mock_response = {
        "tables": [
            {"id": "BE0101A", "label": "Wage statistics"}
        ],
        "page": 1,
        "totalPages": 1,
        "totalHits": 1,
        "links": []
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await search_tables("wage")
        assert result["tables"][0]["id"] == "BE0101A"


@pytest.mark.asyncio
async def test_get_table_data():
    """Test get_table_data function"""
    mock_response = {
        "id": "BE0101A",
        "label": "Population by age and sex",
        "variables": [{"id": "Age", "values": ["15-64"]}],
        "values": [{"key": {"Age": "15-64"}, "values": [{"value": 1000000}]}]
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await get_table_data("BE0101A", filters={"Age": "15-64"})
        assert result["id"] == "BE0101A"
        assert result["values"][0]["values"][0]["value"] == 1000000


@pytest.mark.asyncio
async def test_get_table_metadata():
    """Test get_table_metadata function"""
    mock_response = {
        "id": "BE0101A",
        "label": "Population by age and sex",
        "variables": [
            {"id": "Age", "label": "Age", "values": ["15-64", "65+"]},
            {"id": "Sex", "label": "Sex", "values": ["1", "2"]}
        ],
        "contentVariable": "Population",
        "timeVariable": "Year"
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await get_table_metadata("BE0101A")
        assert result["id"] == "BE0101A"
        assert len(result["variables"]) == 2


@pytest.mark.asyncio
async def test_get_default_selection():
    """Test get_default_selection function"""
    mock_response = {
        "selection": {
            "Age": "15-64",
            "Region": "01"
        }
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await get_default_selection("BE0101A")
        assert result["selection"]["Age"] == "15-64"


@pytest.mark.asyncio
async def test_list_codelists():
    """Test list_codelists function"""
    mock_response = {
        "codelists": [
            {"id": "Region", "label": "Regions"},
            {"id": "Age", "label": "Age groups"}
        ],
        "page": 1,
        "totalPages": 1,
        "totalHits": 2,
        "links": []
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await list_codelists()
        assert len(result["codelists"]) == 2
        assert result["totalHits"] == 2


@pytest.mark.asyncio
async def test_get_codelist():
    """Test get_codelist function"""
    mock_response = {
        "id": "Region",
        "label": "Regions",
        "codes": [
            {"code": "01", "value": "Stockholm"},
            {"code": "02", "value": "Västra Götaland"}
        ]
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await get_codelist("Region")
        assert result["id"] == "Region"
        assert result["codes"][0]["code"] == "01"


@pytest.mark.asyncio
async def test_get_codelist_metadata():
    """Test get_codelist_metadata function"""
    mock_response = {
        "id": "Region",
        "label": "Regions",
        "description": "Administrative regions in Sweden"
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await get_codelist_metadata("Region")
        assert result["id"] == "Region"
        assert "Administrative regions" in result["description"]


@pytest.mark.asyncio
async def test_list_saved_queries():
    """Test list_saved_queries function"""
    mock_response = {
        "queries": [
            {"id": "query1", "label": "My employment query"}
        ],
        "page": 1,
        "totalPages": 1,
        "totalHits": 1,
        "links": []
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await list_saved_queries()
        assert result["queries"][0]["id"] == "query1"


@pytest.mark.asyncio
async def test_get_saved_query():
    """Test get_saved_query function"""
    mock_response = {
        "id": "query1",
        "label": "My employment query",
        "tableId": "BE0101A",
        "selection": {"Age": "15-64"},
        "data": [{"value": 1000000}]
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await get_saved_query("query1")
        assert result["id"] == "query1"
        assert result["tableId"] == "BE0101A"


@pytest.mark.asyncio
async def test_save_query():
    """Test save_query function"""
    mock_response = {
        "id": "query1",
        "label": "My employment query",
        "tableId": "BE0101A",
        "selection": {"Age": "15-64"},
        "links": []
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await save_query("BE0101A", {"Age": "15-64"})
        assert result["id"] == "query1"
        assert result["tableId"] == "BE0101A"


@pytest.mark.asyncio
async def test_delete_saved_query():
    """Test delete_saved_query function"""
    mock_response = {
        "message": "Query deleted successfully"
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        result = await delete_saved_query("query1")
        assert "deleted successfully" in result["message"]


@pytest.mark.asyncio
async def test_api_error_handling():
    """Test that API errors are properly raised"""
    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = SCBAPIError("Invalid table ID")
        with pytest.raises(SCBAPIError):
            await get_table_info("INVALID")


@pytest.mark.asyncio
async def test_rate_limit_handling():
    """Test that rate limit errors are properly raised"""
    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = RateLimitError("Rate limit exceeded")
        with pytest.raises(RateLimitError):
            await get_table_info("BE0101A")


@pytest.mark.asyncio
async def test_language_parameter():
    """Test that language parameter is properly passed"""
    mock_response = {"label": "Population"}

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        await get_table_info("BE0101A", lang="sv")
        # Verify the request was made with Swedish language
        call_args = mock_request.call_args
        assert call_args[1]['params']['lang'] == 'sv'


@pytest.mark.asyncio
async def test_pagination_parameters():
    """Test that pagination parameters are properly passed"""
    mock_response = {
        "tables": [],
        "page": 2,
        "totalPages": 10,
        "totalHits": 100,
        "links": []
    }

    with patch('scb_opendata_mcp.server._request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        await list_tables(page_number=2, page_size=50)
        # Verify the request was made with pagination parameters
        call_args = mock_request.call_args
        assert call_args[1]['params']['page'] == 2
        assert call_args[1]['params']['pagesize'] == 50


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
