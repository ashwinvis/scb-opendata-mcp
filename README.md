# FastMCP Server for Statistics Sweden (SCB) API

A FastMCP server that provides access to Statistics Sweden's PxWeb API v2, offering 5,155 statistical tables covering employment, labor costs, wages, and other economic data from Sweden.

## Features

- **Table Discovery**: Browse and search 5,155 statistical tables
- **Data Retrieval**: Fetch statistical data with optional filtering
- **Codelists**: Access code lists for valid filter values
- **Saved Queries**: Save and retrieve frequently used queries
- **Pagination**: Handle large result sets efficiently
- **Language Support**: English and Swedish
- **Error Handling**: Robust error handling with retry logic

## Installation

### Prerequisites

- Python 3.13 or higher
- pip or uv package manager

### Install from source

```bash
# Clone the repository
git clone https://github.com/yourusername/scb-fastmcp.git
cd scb-fastmcp

# Install dependencies
pip install fastmcp

# Or with uv
uv sync
```

## Usage

### Running the server

```bash
# Run the FastMCP server
python -m scb_fastmcp.main

# Or with uv
uv run scb_fastmcp.main
```

### Using with Claude Code

The server is designed to work with Claude Code's MCP protocol. Once running, you can use tools like:

```python
# List tables about employment
result = await list_tables(query="employment")

# Get detailed info about a specific table
table_info = await get_table_info("BE0101A")

# Retrieve actual data
data = await get_table_data("BE0101A", Age="15-64", Region="01")
```

## Tools Available

### Table Discovery
- `list_tables()` - List all available statistical tables with pagination
- `get_table_info(table_id)` - Get metadata for a specific table
- `search_tables(query)` - Search tables by name or description

### Data Retrieval
- `get_table_data(table_id, **filters)` - Fetch data with optional filtering
- `get_table_metadata(table_id)` - Get detailed metadata including variables
- `get_default_selection(table_id)` - Get default data selection for a table

### Codelist Tools
- `list_codelists()` - List all available codelists
- `get_codelist(codelist_id)` - Get specific codelist details
- `get_codelist_metadata(codelist_id)` - Get metadata for a codelist

### Saved Query Tools
- `list_saved_queries()` - List user's saved queries
- `get_saved_query(query_id)` - Get a specific saved query
- `save_query(table_id, selection)` - Save a data query
- `delete_saved_query(query_id)` - Delete a saved query

## Documentation

- **[Usage Guide](docs/usage.md)** - Examples and best practices for using the server
- **[Tool Documentation](docs/tools.md)** - Detailed documentation for each tool
- **[API Specs](docs/specs.md)** - Conceptual documentation about the PxAPI
- **[OpenAPI Specification](docs/PxAPI-2.yml)** - Technical API specification

## Examples

### Finding Employment Data

```python
# Search for employment tables
results = await search_tables("employment", page_size=20)

# Get details about the first table
table_id = results['tables'][0]['id']
table_info = await get_table_info(table_id)

# Get metadata to understand variables
metadata = await get_table_metadata(table_id)

# Retrieve data for Stockholm (region code 01)
stockholm_data = await get_table_data(
    table_id,
    Region="01",
    Age="15-64"
)
```

### Working with Codelists

```python
# Get region codelist
regions = await get_codelist("Region")

# Get age groups
age_groups = await get_codelist("Age")

# Use in a query
stockholm_data = await get_table_data(
    "BE0101A",
    Region="01",  # Stockholm
    Age="15-64"
)
```

### Saving Queries

```python
# Save a common query
saved = await save_query(
    "BE0101A",
    {"Age": "15-64", "Region": "01"}
)

# Retrieve it later
saved_data = await get_saved_query(saved["id"])
```

## API Information

- **Base URL**: https://api.scb.se/OV0104/v2
- **Rate Limit**: 30 requests per 10 seconds
- **Max Data Cells**: 10,000 per request
- **Supported Languages**: English (en), Swedish (sv)

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest tests/
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Support

For issues or questions:
- Check the [documentation](docs/)
- Review the [OpenAPI specification](docs/PxAPI-2.yml)
- Visit [Statistics Sweden API documentation](https://www.scb.se/en/services/api-intro)
