---
name: scb-opendata-mcp-workflows
description: Use cases and workflows to show how to invoke a tool, or chain multiple tools in the MCP scb-opendata-mcp
---

# SCB Open-data MCP server


## Use Cases & Examples

### Find Employment Data for Stockholm

```
1. search_tables(query="employment")
2. get_table_info(table_id="BE0101A")
3. get_table_data(table_id="BE0101A", Region="01", Age="15-64")
```

### Compare Employment Data Across Regions

```
1. search_tables(query="employment")
2. get_table_info(table_id="BE0101A")
3. get_table_data(table_id="BE0101A", Region="01", Age="15-64")
4. get_table_data(table_id="BE0101A", Region="02", Age="15-64")
```

### Save and Retrieve a Common Query

```
1. save_query(table_id="BE0101A", selection={"Region": "01", "Age": "15-64"})
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
1. get_table_metadata(table_id="BE0101A")
2. get_default_selection(table_id="BE0101A")
```

### Search and Retrieve Data with Pagination

```
1. search_tables(query="wage", page_size=20)
2. get_table_info(table_id="wage-table-id")
3. get_table_data(table_id="wage-table-id", filters={"Age": "15-64"})
```

### Retrieve Population Data by Age and Sex

```
1. search_tables(query="population")
2. get_table_info(table_id="population-table-id")
3. get_table_data(table_id="population-table-id", Age="15-64", Sex="1")
```

### Analyze Labor Costs Across Different Sectors

```
1. search_tables(query="labor costs")
2. get_table_info(table_id="labor-costs-table-id")
3. get_table_data(table_id="labor-costs-table-id", Sector="private", Year="2023")
```


