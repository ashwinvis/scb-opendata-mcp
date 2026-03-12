from fastmcp import FastMCP
import httpx
import time
from typing import Optional, Dict, Any, List
import json

# API Configuration
API_BASE_URL = "https://statistikdatabasen.scb.se/api/v2/"
DEFAULT_LANGUAGE = "en"
MAX_RETRIES = 3
RETRY_DELAY = 1.0

mcp = FastMCP("FastMCP server for scb.se (Statistics Sweden) 🚀")

class SCBAPIError(Exception):
    """Custom exception for SCB API errors"""
    pass

class RateLimitError(Exception):
    """Custom exception for rate limit errors"""
    pass

async def _request(
    method: str,
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    retry_count: int = 0
) -> Dict[str, Any]:
    """
    Internal method to make HTTP requests to SCB API with retry logic.

    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint path
        params: Query parameters
        json_data: JSON data for POST requests
        headers: HTTP headers
        retry_count: Current retry attempt count

    Returns:
        Response JSON data

    Raises:
        SCBAPIError: For API errors
        RateLimitError: For rate limit errors
    """
    url = f"{API_BASE_URL}{endpoint}"

    # Default headers
    default_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    if headers:
        default_headers.update(headers)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=default_headers,
                timeout=30.0
            )

            # Check for rate limiting
            if response.status_code == 429:
                if retry_count < MAX_RETRIES:
                    retry_after = float(response.headers.get("Retry-After", RETRY_DELAY))
                    time.sleep(retry_after)
                    return await _request(
                        method, endpoint, params, json_data, headers, retry_count + 1
                    )
                raise RateLimitError("Rate limit exceeded after retries")

            # Check for other errors
            if response.status_code >= 400:
                error_msg = f"API request failed with status {response.status_code}"
                try:
                    error_data = response.json()
                    if "message" in error_data:
                        error_msg += f": {error_data['message']}"
                except:
                    pass
                raise SCBAPIError(error_msg)

            return response.json()

        except httpx.HTTPError as e:
            raise SCBAPIError(f"HTTP error occurred: {str(e)}")
        except json.JSONDecodeError:
            raise SCBAPIError("Invalid JSON response from API")

# ============================================================================
# TABLE DISCOVERY TOOLS
# ============================================================================

@mcp.tool()
async def list_tables(
    lang: str = DEFAULT_LANGUAGE,
    query: Optional[str] = None,
    past_days: Optional[int] = None,
    include_discontinued: bool = False,
    page_number: int = 1,
    page_size: int = 100
) -> Dict[str, Any]:
    """
    List all available statistical tables from Statistics Sweden.

    This tool allows you to browse the 5,155 statistical tables covering employment,
    labor costs, wages, and other economic data. You can filter by search query,
    limit to recently updated tables, and control pagination.

    Args:
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.
        query: Search query to filter tables by name or description.
        past_days: Only show tables updated in the last N days.
        include_discontinued: Include discontinued tables in results.
        page_number: Page number for pagination (1-based).
        page_size: Number of results per page (max 100).

    Returns:
        Dictionary containing:
        - tables: List of table information objects
        - page: Current page number
        - total_pages: Total number of pages
        - total_hits: Total number of matching tables
        - links: Pagination links

    Example:
        List employment tables:
        ```
        list_tables(query="employment")
        ```

        Get 50 results per page:
        ```
        list_tables(page_size=50)
        ```
    """
    params = {
        "lang": lang,
        "page": page_number,
        "pagesize": page_size
    }

    if query:
        params["query"] = query
    if past_days:
        params["pastDays"] = past_days
    if include_discontinued:
        params["includeDiscontinued"] = "true"

    data = await _request("GET", "/tables", params=params)
    return data

@mcp.tool()
async def get_table_info(
    table_id: str,
    lang: str = DEFAULT_LANGUAGE
) -> Dict[str, Any]:
    """
    Get detailed information about a specific statistical table.

    This tool provides metadata for a specific table including its description,
    update frequency, and other key information. Use this to understand what
    data a table contains before retrieving it.

    Args:
        table_id: The ID of the table to retrieve (e.g., "BE0101A")
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.

    Returns:
        Dictionary containing:
        - id: Table identifier
        - label: Table name/title
        - description: Table description
        - contentType: Type of content (e.g., "Data")
        - updateFrequency: How often the table is updated
        - lastUpdated: When the table was last updated
        - nextUpdate: When the table will be updated next
        - variables: List of variables in the table
        - links: Related links

    Example:
        Get info about employment table:
        ```
        get_table_info("BE0101A")
        ```
    """
    data = await _request("GET", f"/tables/{table_id}", params={"lang": lang})
    return data

@mcp.tool()
async def search_tables(
    query: str,
    lang: str = DEFAULT_LANGUAGE,
    page_number: int = 1,
    page_size: int = 50
) -> Dict[str, Any]:
    """
    Search statistical tables by name or description.

    This is a convenience wrapper around list_tables that focuses on the search
    functionality. Use this when you want to quickly find tables matching specific
    keywords.

    Args:
        query: Search query to filter tables
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.
        page_number: Page number for pagination (1-based).
        page_size: Number of results per page (max 100).

    Returns:
        Dictionary containing search results with tables matching the query.

    Example:
        Search for wage tables:
        ```
        search_tables("wage statistics")
        ```

        Search for employment by region:
        ```
        search_tables("employment region")
        ```
    """
    return await list_tables(
        lang=lang,
        query=query,
        page_number=page_number,
        page_size=page_size
    )

# ============================================================================
# DATA RETRIEVAL TOOLS
# ============================================================================

@mcp.tool()
async def get_table_data(
    table_id: str,
    lang: str = DEFAULT_LANGUAGE,
    **filters
) -> Dict[str, Any]:
    """
    Retrieve statistical data from a table with optional filtering.

    This is the main tool for fetching actual data. You can specify which
    dimensions/variables you want to include using filter parameters.

    Args:
        table_id: The ID of the table to retrieve data from
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.
        **filters: Optional filters for specific variables. Format:
            - For single values: `variableId=value`
            - For multiple values: `variableId=[value1, value2]`
            - Example: `Age=15-19`, `Region=01` (Stockholm)

    Returns:
        Dictionary containing:
        - id: Table identifier
        - label: Table name
        - variables: Variable definitions
        - values: The actual statistical data
        - dimensions: Dimension information

    Example:
        Get basic data from a table:
        ```
        get_table_data("BE0101A")
        ```

        Filter by age group and region:
        ```
        get_table_data("BE0101A", Age="15-64", Region="01")
        ```

        Filter with multiple values:
        ```
        get_table_data("BE0101A", Age=["15-24", "25-54"], Region="01")
        ```
    """
    # Build the query parameter
    query = {}
    for var_name, var_value in filters.items():
        if isinstance(var_value, list):
            # Multiple values
            query[var_name] = [str(v) for v in var_value]
        else:
            # Single value
            query[var_name] = str(var_value)

    params = {"lang": lang}
    json_data = {"query": [query], "response": {"format": "json"}}

    data = await _request("POST", f"/tables/{table_id}/code", json_data=json_data, params=params)
    return data

@mcp.tool()
async def get_table_metadata(
    table_id: str,
    lang: str = DEFAULT_LANGUAGE,
    default_selection: bool = False,
    saved_query: Optional[str] = None,
    codelist: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Get detailed metadata for a table including all variables and values.

    This tool provides comprehensive metadata needed to understand and query
    a table, including all variables, their possible values, and relationships.
    Use this before retrieving data to understand what filters you can apply.

    Args:
        table_id: The ID of the table
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.
        default_selection: Whether to include default selection
        saved_query: Optional saved query ID to apply
        codelist: Optional codelist to apply

    Returns:
        Dictionary containing:
        - id: Table identifier
        - label: Table name
        - variables: Detailed variable definitions with values
        - contentVariable: The main content variable
        - timeVariable: The time dimension variable
        - links: Related links

    Example:
        Get full metadata for a table:
        ```
        get_table_metadata("BE0101A")
        ```
    """
    params = {"lang": lang}
    if default_selection:
        params["defaultSelection"] = "true"
    if saved_query:
        params["savedQuery"] = saved_query
    if codelist:
        # Convert dict to query string format
        codelist_str = ",".join([f"{k}={v}" for k, v in codelist.items()])
        params["codelist"] = codelist_str

    data = await _request("GET", f"/tables/{table_id}/metadata", params=params)
    return data

@mcp.tool()
async def get_default_selection(
    table_id: str,
    lang: str = DEFAULT_LANGUAGE
) -> Dict[str, Any]:
    """
    Get the default data selection for a table.

    This shows you what data would be returned if you made a basic query
    without specifying any filters. Useful for understanding typical usage
    of a table.

    Args:
        table_id: The ID of the table
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.

    Returns:
        Dictionary containing the default selection criteria and expected
        data structure.

    Example:
        Get default selection for employment table:
        ```
        get_default_selection("BE0101A")
        ```
    """
    data = await _request("GET", f"/tables/{table_id}/defaultselection", params={"lang": lang})
    return data

# ============================================================================
# CODELIST TOOLS
# ============================================================================

@mcp.tool()
async def list_codelists(
    lang: str = DEFAULT_LANGUAGE,
    page_number: int = 1,
    page_size: int = 100
) -> Dict[str, Any]:
    """
    List all available codelists.

    Codelists define the values that variables can take. They allow you to
    group or categorize data in different ways (e.g., by county instead of
    municipality).

    Args:
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.
        page_number: Page number for pagination (1-based).
        page_size: Number of results per page (max 100).

    Returns:
        Dictionary containing:
        - codelists: List of codelist information
        - page: Current page number
        - total_pages: Total number of pages
        - total_hits: Total number of codelists

    Example:
        List all codelists:
        ```
        list_codelists()
        ```
    """
    params = {
        "lang": lang,
        "page": page_number,
        "pagesize": page_size
    }

    data = await _request("GET", "/codelists", params=params)
    return data

@mcp.tool()
async def get_codelist(
    codelist_id: str,
    lang: str = DEFAULT_LANGUAGE
) -> Dict[str, Any]:
    """
    Get a specific codelist with all its values.

    Codelists map codes to human-readable labels. For example, region code
    "01" maps to "Stockholm". Use this to understand what values are valid
    for filtering.

    Args:
        codelist_id: The ID of the codelist
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.

    Returns:
        Dictionary containing:
        - id: Codelist identifier
        - label: Codelist name
        - codes: List of code-value pairs
        - variables: Variables this codelist applies to

    Example:
        Get region codelist:
        ```
        get_codelist("Region")
        ```
    """
    data = await _request("GET", f"/codelists/{codelist_id}", params={"lang": lang})
    return data

@mcp.tool()
async def get_codelist_metadata(
    codelist_id: str,
    lang: str = DEFAULT_LANGUAGE
) -> Dict[str, Any]:
    """
    Get metadata for a specific codelist.

    This provides additional information about a codelist such as its purpose
    and usage context.

    Args:
        codelist_id: The ID of the codelist
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.

    Returns:
        Dictionary containing codelist metadata.

    Example:
        Get metadata for age codelist:
        ```
        get_codelist_metadata("Age")
        ```
    """
    data = await _request("GET", f"/codelists/{codelist_id}/metadata", params={"lang": lang})
    return data

# ============================================================================
# SAVED QUERY TOOLS
# ============================================================================

@mcp.tool()
async def list_saved_queries(
    lang: str = DEFAULT_LANGUAGE,
    page_number: int = 1,
    page_size: int = 50
) -> Dict[str, Any]:
    """
    List all saved queries for the current user.

    Saved queries allow you to store specific data selections so you can
    quickly retrieve the same data later without re-specifying all filters.

    Args:
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.
        page_number: Page number for pagination (1-based).
        page_size: Number of results per page (max 100).

    Returns:
        Dictionary containing:
        - queries: List of saved query information
        - page: Current page number
        - total_pages: Total number of pages
        - total_hits: Total number of saved queries

    Example:
        List saved queries:
        ```
        list_saved_queries()
        ```
    """
    params = {
        "lang": lang,
        "page": page_number,
        "pagesize": page_size
    }

    data = await _request("GET", "/savedqueries", params=params)
    return data

@mcp.tool()
async def get_saved_query(
    query_id: str,
    lang: str = DEFAULT_LANGUAGE
) -> Dict[str, Any]:
    """
    Get a specific saved query.

    Retrieve the data selection and results from a previously saved query.

    Args:
        query_id: The ID of the saved query
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.

    Returns:
        Dictionary containing:
        - id: Query identifier
        - label: Query name
        - tableId: ID of the table this query applies to
        - selection: The data selection criteria
        - data: The retrieved data

    Example:
        Get a saved query:
        ```
        get_saved_query("my-query-123")
        ```
    """
    data = await _request("GET", f"/savedqueries/{query_id}", params={"lang": lang})
    return data

@mcp.tool()
async def save_query(
    table_id: str,
    selection: Dict[str, Any],
    lang: str = DEFAULT_LANGUAGE
) -> Dict[str, Any]:
    """
    Save a data query for later use.

    This allows you to store a specific data selection so you can quickly
    retrieve the same data later. The saved query includes both the selection
    criteria and the retrieved data.

    Args:
        table_id: The ID of the table
        selection: The data selection criteria (variable filters)
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.

    Returns:
        Dictionary containing:
        - id: The saved query ID
        - label: Query name
        - tableId: ID of the table
        - selection: The saved selection criteria
        - links: Related links

    Example:
        Save a query for employment data:
        ```
        save_query("BE0101A", {"Age": "15-64", "Region": "01"})
        ```
    """
    json_data = {
        "tableId": table_id,
        "selection": selection
    }

    data = await _request(
        "POST", "/savedqueries",
        json_data=json_data,
        params={"lang": lang}
    )
    return data

@mcp.tool()
async def delete_saved_query(
    query_id: str,
    lang: str = DEFAULT_LANGUAGE
) -> Dict[str, Any]:
    """
    Delete a saved query.

    Remove a previously saved query and its associated data.

    Args:
        query_id: The ID of the saved query to delete
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.

    Returns:
        Dictionary confirming the deletion.

    Example:
        Delete a saved query:
        ```
        delete_saved_query("my-query-123")
        ```
    """
    data = await _request(
        "DELETE", f"/savedqueries/{query_id}",
        params={"lang": lang}
    )
    return data
