---
name: scb-opendata-mcp-workflows
description: Use cases and workflows to show how to invoke a tool, or chain multiple tools in the MCP scb-opendata-mcp
---

# SCB Open-data MCP server

## Use Cases & Examples

### Find Employment Data for Stockholm

```
1. search_tables(query="employment", lang="en")
2. get_table_info(table_id="TAB4707")
3. get_table_data(table_id="TAB4707", filters={"region": "01", "age": "15-64"})
```

### Compare Employment Data Across Regions

```
1. search_tables(query="employment", lang="en")
2. get_table_info(table_id="TAB4707")
3. get_table_data(table_id="TAB4707", filters={"region": "01", "age": "15-64"})
4. get_table_data(table_id="TAB4707", filters={"region": "02", "age": "15-64"})
```

### Save and Retrieve a Common Query

```
1. save_query(table_id="TAB4707", selection={"region": "01", "age": "15-64"})
2. list_saved_queries()
3. get_saved_query(query_id="saved-query-id")
```

### Explore Available Codelists

```
1. list_codelists()
2. get_codelist(codelist_id="Region")
3. get_codelist(codelist_id="Age")
```

### Get Detailed Metadata for a Table

```
1. get_table_metadata(table_id="TAB4707")
2. get_default_selection(table_id="TAB4707")
```

### Search and Retrieve Data with Pagination

```
1. search_tables(query="wage", lang="en", page_size=20)
2. get_table_info(table_id="TAB6047")
3. get_table_data(table_id="TAB6047", filters={"age": "15-64"})
```

### Retrieve Population Data by Age and Sex

```
1. search_tables(query="population", lang="en")
2. get_table_info(table_id="TAB6008")
3. get_table_data(table_id="TAB6008", filters={"age": "15-64", "sex": "1"})
```

### Analyze Labor Costs Across Different Sectors

```
1. search_tables(query="labor cost", lang="en")
2. get_table_info(table_id="TAB68")
3. get_table_data(table_id="TAB68", filters={"sector": "private", "year": "2023"})
```