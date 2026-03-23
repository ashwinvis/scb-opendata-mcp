# MCP Server for Statistics Sweden (SCB) API

[![PyPI](https://img.shields.io/pypi/v/scb-opendata-mcp)](https://pypi.org/project/scb-opendata-mcp/)

A FastMCP server that provides access to Statistics Sweden's PxWebApi v2, offering statistical tables covering employment, labor costs, wages, and other civil data from Sweden.

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

- Python 3.11 or higher
- pip or uv package manager

### Install from PyPI

```bash
pip install scb-opendata-mcp

# Or with uv
uvx scb_opendata_mcp
```

### Install from source

```bash
# Clone the repository
git clone https://github.com/ashwinvis/scb-opendata-mcp.git
cd scb-opendata-mcp

# Install dependencies
pip install .

# Or with uv
uv sync
```

## Usage

### Running the server

The package on installation 

```bash
scb_opendata_mcp

# Or with uv
uv run scb_opendata_mcp
```

See `scb_opendata_mcp --help` for available options. An `stdio` transport mechanism also exists.

**Fallback option**

```bash
uv run fastmcp run src/scb_opendata_mcp/server.py -t http  # HTTP server
```

## Configuration for common agent harnesses

### Claude Code

```bash
claude mcp add --scope user --transport http scb_opendata_mcp http://localhost:6767
```

### Mistral Vibe

In `~/.vibe/config.toml` or `~/.vibe/agents/name_of_agent.toml`:

```toml
[[mcp_servers]]
name = "scb_opendata_mcp"
transport = "http"
url = "http://localhost:6767/mcp"
```

### OpenCode

In `~/.config/opencode/opencode.jsonc`:

```json
{
  "mcp": {
    "scb_opendata_mcp": {
      "type": "remote",
      "url": "https://localhost:6767/mcp",
      "enabled": true
    }
  }
}
```

## Tools Available

### Table Discovery
- `list_tables()` - List all available statistical tables with pagination
- `get_table_metadata(table_id)` - Get detailed metadata including variables
- `search_tables(query)` - Convenience wrapper over `list_tables`, to search tables by name or description

### Data Retrieval
- `get_table_data(table_id, filters)` - Fetch data with optional filtering
- `get_table_default_selection(table_id)` - Get default data selection for a table

### Codelist Tools
- `list_codelists(table_id)` - List all available codelists for the table
- `get_codelist(codelist_id)` - Get specific codelist details

### Saved Query Tools
- `get_saved_query(query_id)` - Get a saved query including data and selection criteria
- `get_saved_query_data(query_id)` - Get data from a specific saved query
- `get_saved_query_selection(query_id)` - Get the selection query used in a specific saved query
- `save_query(table_id, selection)` - Save a data query
- `delete_saved_query(query_id)` - Delete a saved query

## Development

### Running Tests

```bash
uv run pytest
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Support

For issues or questions:
- Review the [OpenAPI specification](docs/PxAPI-2.yml) or alternatively from <https://github.com/PxTools/PxApiSpecs/blob/master/PxAPI-2.yml>.
- Visit Statistics Sweden API documentation:
  - På svenska: <https://www.scb.se/vara-tjanster/oppna-data/pxwebapi/pxwebapi-v2/>
  - In English: <https://www.scb.se/en/services/open-data-api/pxwebapi/>

## SCB Open Data Skills

This is an unofficial companion repository [SCB Open Data Skills](https://github.com/ashwinvis/scb-opendata-skills) that provides skill definitions for accessing Statistics Sweden's data through this MCP server. These skills are designed to work with major coding agent tools and provide workflows for various statistical domains.

## Disclaimer

This is an unofficial tool. The code was generated using AI while using official documents and the API specification as context.
Tests are also added to verify the functionality. A thorough rigorous verification test is recommended before using it in any
serious application.
