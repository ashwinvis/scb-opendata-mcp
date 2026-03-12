---
name: scb-labor-market
description: Workflows and use cases for SCB Labor Market tables covering employment, wages, working hours, and labor costs
---

# SCB Labor Market Tables

This skill provides workflows for accessing Statistics Sweden's comprehensive labor market data, including employment statistics, wage information, working hours, labor costs, and related economic indicators.

## Common Table IDs and Keywords

- **Employment Statistics**: TAB4707, TAB4714, TAB4718, TAB4723 (keywords: "employment", "anställningar", "ongoing employments")
- **Wage Data**: TAB6047, TAB6048 (keywords: "wages", "lönesummor", "salary sums")
- **Working Hours**: TAB5191, TAB6650 (keywords: "working hours", "arbetad tid", "hours worked")
- **Labor Costs**: TAB68, TAB72 (keywords: "labor costs", "arbetskostnadsindex", "labor cost index")
- **Sickness Absence**: TAB6458, TAB6467, TAB6468 (keywords: "sickness absence", "sjukfrånvaro")
- **Employment Flow**: TAB6012, TAB6016 (keywords: "employment flow", "flöde anställningar")

## Use Cases & Examples

### Find Current Employment Statistics by Sector
```
1. search_tables(query="employment", lang="en")
2. get_table_info(table_id="TAB4707")
3. get_table_data(table_id="TAB4707", filters={"sektor": "privat", "månad": "2025M12"})
```

### Compare Wages Across Public and Private Sectors
```
1. search_tables(query="wages", lang="en")
2. get_table_metadata(table_id="TAB6047")
3. get_table_data(table_id="TAB6047", filters={"sektor": "privat", "år": "2024"})
4. get_table_data(table_id="TAB6047", filters={"sektor": "offentlig", "år": "2024"})
```

### Analyze Working Hours Trends by Industry
```
1. search_tables(query="working hours", lang="en")
2. get_table_info(table_id="TAB5191")
3. get_table_data(table_id="TAB5191", filters={"sektor": "privat", "näringsgren": "C", "kvartal": "2024K4"})
```

### Retrieve Labor Cost Index for Economic Analysis
```
1. search_tables(query="labor cost", lang="en")
2. get_table_info(table_id="TAB68")
3. get_table_data(table_id="TAB68", filters={"år": "2024", "kvartal": "K4"})
```

### Compare Employment by Gender and Region
```
1. search_tables(query="employment", lang="en")
2. get_table_info(table_id="TAB4718")
3. get_codelist(codelist_id="Region")
4. get_table_data(table_id="TAB4718", filters={"kön": "1", "region": "01", "år": "2024"})
5. get_table_data(table_id="TAB4718", filters={"kön": "2", "region": "01", "år": "2024"})
```

### Analyze Sickness Absence Patterns
```
1. search_tables(query="sickness", lang="en")
2. get_table_info(table_id="TAB6458")
3. get_table_data(table_id="TAB6458", filters={"sektor": "privat", "år": "2024", "kvartal": "K1-K4"})
```

### Examine Employment Flow and Turnover
```
1. search_tables(query="employment flow", lang="en")
2. get_table_info(table_id="TAB6012")
3. get_table_data(table_id="TAB6012", filters={"kön": "1+2", "storleksklass": "10-49", "år": "2024"})
```

### Retrieve Industry-Specific Employment Data
```
1. search_tables(query="employment", lang="en")
2. get_table_info(table_id="TAB4723")
3. get_codelist(codelist_id="SNI2007")
4. get_table_data(table_id="TAB4723", filters={"näringsgren": "C", "år": "2024", "månad": "M12"})
```