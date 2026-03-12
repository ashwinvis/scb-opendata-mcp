---
name: scb-housing-construction
description: Workflows and use cases for SCB Housing and Construction tables covering real estate, building permits, and construction statistics
---

# SCB Housing and Construction Tables

This skill provides workflows for accessing Statistics Sweden's housing and construction data, including real estate transactions, building permits, construction costs, property taxes, and housing market indicators.

## Common Table IDs and Keywords

- **Building Permits**: TAB513, TAB2534, TAB796 (keywords: "building permits", "bygglov", "construction permits")
- **Housing Starts**: TAB513, TAB2534 (keywords: "housing starts", "påbörjade bostäder", "new constructions")
- **Housing Completions**: TAB4384, TAB4385 (keywords: "housing completions", "färdigställda bostäder", "completed housing")
- **Real Estate Prices**: TAB4711, TAB4712, TAB1143 (keywords: "real estate prices", "bostadspriser", "property prices")
- **Construction Costs**: TAB4410, TAB1368 (keywords: "construction costs", "byggkostnader", "building costs")
- **Property Taxes**: TAB4711, TAB4712 (keywords: "property taxes", "fastighetsskatt", "real estate taxes")

## Use Cases & Examples

### Retrieve Current Building Permit Statistics
```
1. search_tables(query="building permits", lang="en")
2. get_table_info(table_id="TAB513")
3. get_table_data(table_id="TAB513", filters={"byggnadstyp": "bostadshus", "år": "2024"})
```

### Analyze Housing Start Trends by Region
```
1. search_tables(query="housing starts", lang="en")
2. get_table_info(table_id="TAB513")
3. get_table_data(table_id="TAB513", filters={"region": "01", "år": "2020-2024"})
```

### Examine Housing Completion Rates
```
1. search_tables(query="housing completions", lang="en")
2. get_table_info(table_id="TAB4384")
3. get_table_data(table_id="TAB4384", filters={"bostadstyp": "flerbostadshus", "år": "2024"})
```

### Retrieve Real Estate Price Index
```
1. search_tables(query="real estate prices", lang="en")
2. get_table_info(table_id="TAB4711")
3. get_table_data(table_id="TAB4711", filters={"bostadstyp": "småhus", "år": "2024"})
```

### Analyze Construction Cost Trends
```
1. search_tables(query="construction costs", lang="en")
2. get_table_info(table_id="TAB4410")
3. get_table_data(table_id="TAB4410", filters={"byggnadstyp": "bostadshus", "år": "2020-2024"})
```

### Compare Property Taxes Across Municipalities
```
1. search_tables(query="property taxes", lang="en")
2. get_table_info(table_id="TAB4711")
3. get_codelist(codelist_id="Kommun")
4. get_table_data(table_id="TAB4711", filters={"kommun": "0180,0140", "år": "2024"})
```

### Examine Housing Market Indicators
```
1. search_tables(query="housing market", lang="en")
2. get_table_info(table_id="TAB4711")
3. get_table_data(table_id="TAB4711", filters={"region": "01", "år": "2024", "kvartal": "K1-K4"})
```

### Analyze Construction Activity by Building Type
```
1. search_tables(query="building permits", lang="en")
2. get_table_info(table_id="TAB513")
3. get_codelist(codelist_id="Byggnadstyp")
4. get_table_data(table_id="TAB513", filters={"byggnadstyp": "bostadshus,icke-bostadshus", "år": "2024"})
```