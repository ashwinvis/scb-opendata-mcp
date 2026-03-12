---
name: scb-population
description: Workflows and use cases for SCB Population tables covering demographics, births, deaths, and population projections
---

# SCB Population Tables

This skill provides workflows for accessing Statistics Sweden's population data, including demographic statistics, birth and death records, population projections, migrations, and household compositions.

## Common Table IDs and Keywords

- **Population Statistics**: TAB6008, TAB698, TAB4161 (keywords: "population", "befolkning", "demographics")
- **Births**: TAB5959, TAB694 (keywords: "births", "födda", "natality")
- **Deaths**: TAB5958, TAB694 (keywords: "deaths", "döda", "mortality")
- **Population Projections**: TAB5974, TAB698 (keywords: "population projections", "befolkningsframskrivningar")
- **Migrations**: TAB698, TAB694 (keywords: "migrations", "flyttningar", "immigration")
- **Households**: TAB4374, TAB1533, TAB1531 (keywords: "households", "hushåll", "family composition")

## Use Cases & Examples

### Retrieve Current Population Statistics by Region
```
1. search_tables(query="population", lang="en")
2. get_table_info(table_id="TAB6008")
3. get_table_data(table_id="TAB6008", filters={"region": "01", "år": "2024"})
```

### Analyze Birth Trends Over Time
```
1. search_tables(query="births", lang="en")
2. get_table_info(table_id="TAB5959")
3. get_table_data(table_id="TAB5959", filters={"år": "2010-2024", "månad": "M01-M12"})
```

### Examine Mortality Rates by Age Group
```
1. search_tables(query="deaths", lang="en")
2. get_table_info(table_id="TAB5958")
3. get_table_data(table_id="TAB5958", filters={"ålder": "0-14", "år": "2024"})
4. get_table_data(table_id="TAB5958", filters={"ålder": "65+", "år": "2024"})
```

### Retrieve Population Projections for Planning
```
1. search_tables(query="population projections", lang="en")
2. get_table_info(table_id="TAB5974")
3. get_table_data(table_id="TAB5974", filters={"scenario": "huvud", "år": "2025-2050"})
```

### Analyze Migration Patterns
```
1. search_tables(query="migration", lang="en")
2. get_table_info(table_id="TAB698")
3. get_table_data(table_id="TAB698", filters={"flyttningstyp": "inflyttning", "år": "2024"})
```

### Examine Household Composition
```
1. search_tables(query="households", lang="en")
2. get_table_info(table_id="TAB4374")
3. get_table_data(table_id="TAB4374", filters={"hushållstyp": "ensam", "år": "2024"})
```

### Compare Population Growth Across Regions
```
1. search_tables(query="population", lang="en")
2. get_table_info(table_id="TAB6008")
3. get_codelist(codelist_id="Region")
4. get_table_data(table_id="TAB6008", filters={"region": "01", "år": "2020,2024"})
5. get_table_data(table_id="TAB6008", filters={"region": "02", "år": "2020,2024"})
```

### Analyze Demographic Changes Over Decades
```
1. search_tables(query="population", lang="en")
2. get_table_info(table_id="TAB698")
3. get_table_data(table_id="TAB698", filters={"år": "1990,2000,2010,2020", "ålder": "0-14,15-64,65+"})
```