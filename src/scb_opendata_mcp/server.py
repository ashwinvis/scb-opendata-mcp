import asyncio
import json
import sys
from typing import Any

import httpx
from fastmcp import FastMCP

from scb_opendata_mcp._version import __version__
from scb_opendata_mcp.models import (
    CodelistResponse,
    CodelistsResponse,
    Dataset,
    OutputFormatParams,
    SavedQueryResponse,
    SelectionResponse,
    TablesResponse,
)


# API Configuration
API_BASE_URL = "https://statistikdatabasen.scb.se/api/v2"
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
    params: dict[str, Any] | None = None,
    json_data: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    retry_count: int = 0,
) -> dict[str, Any]:
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
        "Content-Type": "application/json",
        "User-Agent": f"scb-opendata-mcp {__version__} Python {sys.version}",
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
                timeout=30.0,
            )

            # Check for rate limiting
            if response.status_code == 429:
                if retry_count < MAX_RETRIES:
                    retry_after = float(
                        response.headers.get("Retry-After", RETRY_DELAY)
                    )
                    await asyncio.sleep(retry_after)
                    return await _request(
                        method, endpoint, params, json_data, headers, retry_count + 1
                    )
                raise RateLimitError("Rate limit exceeded after retries")

            # Respect X-Rate-Limit headers
            # https://github.com/stefanprodan/aspnetcoreratelimit/wiki/ipratelimitmiddleware#behavior
            if int(response.headers.get("X-Rate-Limit-Remaining", 1)) < 1:
                rate_limit_period = int(
                    response.headers.get("X-Rate-Limit-Limit", "10s").removesuffix("s")
                )
                await asyncio.sleep(rate_limit_period)

            # Check for other errors
            if response.status_code >= 400:
                error_msg = f"API request failed with status {response.status_code}"
                try:
                    error_data = response.json()
                    if "message" in error_data:
                        error_msg += f": {error_data['message']}"
                    if "title" in error_data:
                        error_msg += f" [{error_data['title']}"
                    if "errors" in error_data:
                        error_msg += f" (Errors: {error_data['errors']})"
                except Exception:
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
    query: str | None = None,
    past_days: int | None = None,
    include_discontinued: bool = False,
    page_number: int = 1,
    page_size: int = 100,
) -> TablesResponse:
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
    params = {"lang": lang, "page": page_number, "pagesize": page_size}

    if query:
        params["query"] = query
    if past_days:
        params["pastDays"] = past_days
    if include_discontinued:
        params["includeDiscontinued"] = "true"

    data = await _request("GET", "/tables", params=params)
    return data


@mcp.tool()
async def search_tables(
    query: str, lang: str = DEFAULT_LANGUAGE, page_number: int = 1, page_size: int = 50
) -> TablesResponse:
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
        lang=lang, query=query, page_number=page_number, page_size=page_size
    )


@mcp.tool()
async def get_table_metadata(
    table_id: str,
    lang: str = DEFAULT_LANGUAGE,
    default_selection: bool = False,
    saved_query: str | None = None,
    codelist: list[dict[str, str]] | None = None,
) -> Dataset:
    """
    Get detailed information about a specific statistical table.

    This tool provides metadata for a specific table including its dimensions,
    size, and other key information. Use this to understand what
    data a table contains before retrieving it.

    Args:
        table_id: The ID of the table
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.
        default_selection: Whether to include default selection as specified in `get_table_default_selection` tool.
        saved_query: Optional saved query ID to apply
        codelist: Optional codelist to apply. If needed, use `list_codelists` to check for available codelists.

    Returns:
        Dataset represents a table's metadata or data according to the JSON-stat 2.0 Dataset Schema.

        Required properties:
        - version: JSON-stat version (always "2.0")
        - class: Class type (always "dataset")
        - id: Table identifier
        - size: Array of integers representing the size of each dimension
        - dimension: Object describing the dimensions of the table. Each dimensions is a dictionary,
          composed of the fields `label`, `note`, `category`, `extension` and `link`.

        Optional properties:
        - href: Link to the resource
        - label: Table name/title
        - source: Source of the data
        - updated: When the table was last updated
        - link: Related links
        - note: Notes for the table
        - role: Role of the dimensions (e.g., time, geo, metric)
        - extension: Additional properties, mostly from PX-file format
        - value: Array of numeric values representing the data
        - status: Object with additional status information

    Example:
        Get full metadata for a table:
        ```
        get_table_metadata("TAB2844")
        ```

        Get metadata for a table and apply a codelist:
        ```
        get_table_metadata("EXAMPLE_TABLE", codelist=[{"variable_1": "NUTS_2008"}])
        ```
    """
    params = {"lang": lang}
    if default_selection:
        params["defaultSelection"] = "true"
    if saved_query:
        params["savedQuery"] = saved_query
    if codelist:
        params["codelist"] = codelist

    data = await _request("GET", f"/tables/{table_id}/metadata", params=params)
    return data


# ============================================================================
# DATA RETRIEVAL TOOLS
# ============================================================================


@mcp.tool()
async def get_table_data(
    table_id: str,
    lang: str = DEFAULT_LANGUAGE,
    selection: list[dict[str, Any]] | None = None,
    output_format: str = "json-stat2",
    output_format_params: OutputFormatParams | None = None,
) -> Dataset:
    """
     Retrieve statistical data from a table with optional filtering.
     It can be useful to explore using `get_table_metadata` and
    `get_table_default_selection` before executing this tool.

     This is the main tool for fetching actual data. You can specify which
     dimensions/variables you want to include using filter parameters.

     Args:
         table_id: The ID of the table to retrieve data from
         lang: Language for responses ('en' or 'sv'). Defaults to 'en'.
         selection: Optional payload for custom selection. It can be a list of dictionaries
             containing the fields `variableCode` and either `codelist` or `valueCodes`.
             valueCodes can be specific lists or a selection expression.
             The syntax for this argument as follows:
             ```
             selection=[
                 {
                     "variableCode": "variable id",
                     "codelist": "",
                     "valueCodes": [
                         "value-code1",
                         "value-code2",
                         "etc"
                     ]
                 }
             ]
             ```
        output_format: Optional output format. If not specified, defaults to 'json-stat2'.
            Available formats include csv,json-stat2,html,parquet,px etc
        output_format_params: Optional parameters for the output format.
            Format-specific parameters to customize the output.

     Returns:
         Dictionary containing:
         - id: Table identifier
         - label: Table name
         - variables: Variable definitions
         - values: The actual statistical data
         - dimensions: Dimension information

     Selection expressions:

         Selection expression can be used to select value codes that matches the expression.
         The following expressions exists:

         - `*` (wildcard)
         - `?` (mask)
         - `top`
         - `bottom`
         - `range`
         - `to`
         - `from`

         ##### `*` (wildcard)

         This matches based on a criteria that contains 1 or 2 wildcards e.g.

         - `*` selects all codes.
         - `12*` select all codes that starts with *12*.
         - `*2` selects all codes that ends with *2*.
         - `*4*` select all codes that contains a *4*.

         ##### `?` (mask)

         This matches on a criteria that contains a question mark e.g.

         - `??` selects all codes that are two characters long.
         - `1?` select all codes that are two characters long and starts with `1`.

         ##### top

         This expression selects the top number of values. If the variable is the time
         variable that will be the latest time periods otherwise it will be the first code
         as specified in the metadata.

         The syntax of the experssion is:

         ```
         top(numberOfValues, offset)
         ```

         where `numberOfValues` specifies the number of values codes that should be
         selected from the top and `offset` is an optional offset from the top. E.g.

         - `top(5)` will select the first 5 values.
         - `top(5, 1)` will skip the first value and select the next 5 values.

         ##### bottom

         This expression selects the bottom number of values. If the variable is the time
         variable that will be the first time periods otherwise it will be the last code
         as specified in the metadata.

         The syntax of the experssion is:

         ```
         bottom(numberOfValues, offset)
         ```

         where `numberOfValues` specifies the number of values codes that should be
         selected from the bottom and `offset` is an optional offset from the bottom. E.g.

         - `bottom(5)` will select the last 5 values.
         - `bottom(5, 1)` will skip the last value and select the next 5 values counting
         from the bottom.

         ##### range

         This expression selects all value code between two value codes as they are given
         in the metadata.

         The syntax is in the form

         ```
         range(value-code1, value-code2)
         ```

         Example if you have a time variable that have codes from the year 2000 to 2025
         then `range(2002,2005)` would select the codes for the years 2002 to 2005.

         ##### from

         This expression selects all value code from the specified value code.

         The syntax is in the form

         ```
         from(value-code1)
         ```

         Example if you have a time variable that have codes from the year 2000 to 2025
         then `from(2005)` would select the codes for the 2005 to 2025. When new data
         comes for the year 2026 that will also be included.

         ##### to

         This expression selects all value code the bottom to the specified value code.

         The syntax is in the form

         ```
         to(value-code1)
         ```

         Example if you have a time variable that have codes from the year 2000 to 2025
         then `to(2005)` would select the codes from the 2000 to 2005.

     Example:
         Get basic data from a table:
         ```
         get_table_data("BE0101A")
         ```

         Get data with selection expressions:
         ```
         get_table_data("TAB2844", selection=[
                  {"variableCode": "Miljoomrade", "valueCodes": ["000", "100", "200", "300", "400"]},
                  {"variableCode": "Tid", "valueCodes": ["from(2001)"]}
         ])
         ```

         Specify output format:
         ```
         get_table_data("BE0101A", output_format="csv")
         ```

         Specify output format with parameters:
         ```
         get_table_data("BE0101A", output_format="json", output_format_params=("UseCodes",)
         ```
    """
    # Build params with output format
    params: dict[str, Any] = {"lang": lang, "outputFormat": output_format}

    # Add output format parameters if provided
    if output_format_params:
        params["outputFormatParams"] = list(output_format_params)

    if selection:
        json_data = {"selection": selection}
        data = await _request(
            "POST", f"/tables/{table_id}/data", params=params, json_data=json_data
        )
    else:
        data = await _request("GET", f"/tables/{table_id}/data", params=params)

    return data


@mcp.tool()
async def get_table_default_selection(
    table_id: str, lang: str = DEFAULT_LANGUAGE
) -> SelectionResponse:
    """
    Get the default data selection for a table by id.

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
        get_table_default_selection("BE0101A")
        ```
    """
    data = await _request(
        "GET", f"/tables/{table_id}/defaultselection", params={"lang": lang}
    )
    return data


# ============================================================================
# CODELIST TOOLS
# ============================================================================


@mcp.tool()
async def list_codelists(
    table_id: str, lang: str = DEFAULT_LANGUAGE
) -> CodelistsResponse:
    """
    List all available codelists for a particular table_id.

    Codelists define the values that  can take. They allow you to
    group or categorize data in different ways (e.g., by county instead of
    municipality).

    Args:
        table_id: The ID of the table to retrieve data from
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.

    Returns:
        Dictionary containing:
        - codelists: List of codelist information
        - page: Current page number
        - total_pages: Total number of pages
        - total_hits: Total number of codelists

    Example:
        List all codelists:
        ```
        list_codelists('TAB5974')
        ```
    """
    data = await get_table_metadata(table_id=table_id, lang=lang)
    codelists = {
        dim_key: dim_value["extension"]["codelists"]
        for dim_key, dim_value in data["dimension"].items()
    }
    return codelists


@mcp.tool()
async def get_codelist(
    codelist_id: str, lang: str = DEFAULT_LANGUAGE
) -> CodelistResponse:
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
        Get codelist on aggregated Age intervals:
        ```
        get_codelist("agg_Ålder10år_1")
        ```
    """
    data = await _request("GET", f"/codelists/{codelist_id}", params={"lang": lang})
    return data


# ============================================================================
# SAVED QUERY TOOLS
# ============================================================================


@mcp.tool()
async def get_saved_query(
    query_id: str, lang: str = DEFAULT_LANGUAGE
) -> SavedQueryResponse:
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
    selection: list[dict[str, Any]],
    lang: str = DEFAULT_LANGUAGE,
    output_format: str = "json-stat2",
    output_format_params: OutputFormatParams = ("UseCodes",),
) -> SavedQueryResponse:
    """
    Save a data query for later use.

    This allows you to store a specific data selection so you can quickly
    retrieve the same data later. The saved query includes both the selection
    criteria and the retrieved data.

    Args:
        table_id: The ID of the table
        selection: The data selection criteria (variable filters)
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.
        output_format: Optional output format. If not specified, defaults to 'json-stat2'.
            Available formats can be retrieved using `get_api_config()`.
        output_format_params: Optional parameters for the output format.
            Format-specific parameters to customize the output.

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
        save_query(
            "BE0101A", selection=[
                {"variableCode": "Age", "valueCode":"15-64"},
                {"variableCode: "Region", "valueCode":"01"}
            ]
        )
        ```

        Save a query with specific output format:
        ```
        save_query(
            "BE0101A",
            selection=[{"variableCode": "Age", "valueCode":"15-64"}],
            output_format="csv"
        )
        ```
    """
    json_data = {
        "tableId": table_id,
        "selection": {"selection": selection},
        "language": lang,
        "outputFormat": output_format,
        "outputFormatParams": list(output_format_params),
    }

    data = await _request("POST", "/savedqueries", json_data=json_data)
    return data


@mcp.tool()
async def delete_saved_query(
    query_id: str, lang: str = DEFAULT_LANGUAGE
) -> SavedQueryResponse:
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
    data = await _request("DELETE", f"/savedqueries/{query_id}", params={"lang": lang})
    return data


@mcp.tool()
async def get_saved_query_data(
    query_id: str,
    lang: str = DEFAULT_LANGUAGE,
    output_format: str = "json-stat2",
    output_format_params: OutputFormatParams | None = None,
) -> Dataset:
    """
    Retrieve data by running a saved query.

    This tool executes a previously saved query and returns the resulting data.
    Use this to get the actual statistical data from a saved query without
    having to respecify all the selection criteria.

    Args:
        query_id: The ID of the saved query
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.
        output_format: Output format for the data (json-stat2, csv, xlsx, etc.)
        output_format_params: Optional parameters for the output format

    Returns:
        Dataset containing the query results according to the JSON-stat 2.0 Dataset Schema.

    Example:
        Get data from a saved query:
        ```
        get_saved_query_data("my-query-123")
        ```

        Get data in CSV format:
        ```
        get_saved_query_data("my-query-123", output_format="csv")
        ```
    """
    params = {"lang": lang, "outputFormat": output_format}
    if output_format_params:
        params["outputFormatParams"] = output_format_params

    data = await _request("GET", f"/savedqueries/{query_id}/data", params=params)
    return data


@mcp.tool()
async def get_saved_query_selection(
    query_id: str, lang: str = DEFAULT_LANGUAGE
) -> SelectionResponse:
    """
    Get the selection criteria for a saved query.

    This tool returns the selection criteria (variable filters and placements)
    that were used to create a saved query. The selection expressions are
    transformed into actual value codes.

    Args:
        query_id: The ID of the saved query
        lang: Language for responses ('en' or 'sv'). Defaults to 'en'.

    Returns:
        SelectionResponse containing the selection criteria that would be applied
        when running the saved query.

    Example:
        Get selection criteria for a saved query:
        ```
        get_saved_query_selection("my-query-123")
        ```
    """
    data = await _request(
        "GET", f"/savedqueries/{query_id}/selection", params={"lang": lang}
    )
    return data
