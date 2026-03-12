---
name: scb-environment
description: Workflows and use cases for SCB Environment tables covering climate, energy, waste, and environmental indicators
---

# SCB Environment Tables

This skill provides workflows for accessing Statistics Sweden's environmental data, including climate indicators, energy consumption, waste management, environmental protection, and sustainability metrics.

## Common Table IDs and Keywords

- **Climate Indicators**: TAB5055, TAB5057 (keywords: "climate", "klimat", "greenhouse gases")
- **Energy Consumption**: TAB3571, TAB3819 (keywords: "energy", "energi", "energy consumption")
- **Waste Management**: TAB5058, TAB5059 (keywords: "waste", "avfall", "waste management")
- **Environmental Protection**: TAB2844, TAB2843 (keywords: "environmental protection", "miljövård", "protection expenditures")
- **Water Resources**: TAB5055, TAB5057 (keywords: "water", "vatten", "water consumption")
- **Air Quality**: TAB6489, TAB6490 (keywords: "air quality", "luftkvalitet", "emissions")
- **Sustainability Indicators**: TAB5055, TAB5057 (keywords: "sustainability", "hållbarhet", "SDG indicators")

## Use Cases & Examples

### Retrieve Greenhouse Gas Emission Statistics
```
1. search_tables(query="climate", lang="en")
2. get_table_info(table_id="TAB5055")
3. get_table_data(table_id="TAB5055", filters={"sektor": "transporter,näringsliv,hushåll", "år": "2024"})
```

### Analyze Energy Consumption by Source
```
1. search_tables(query="energy", lang="en")
2. get_table_info(table_id="TAB3571")
3. get_table_data(table_id="TAB3571", filters={"energikälla": "fossil,förnybar", "år": "2024"})
```

### Examine Waste Management Statistics
```
1. search_tables(query="waste", lang="en")
2. get_table_info(table_id="TAB5058")
3. get_table_data(table_id="TAB5058", filters={"avfallstyp": "hushåll,näringsliv", "år": "2024"})
```

### Retrieve Environmental Protection Expenditures
```
1. search_tables(query="environmental protection", lang="en")
2. get_table_info(table_id="TAB2844")
3. get_table_data(table_id="TAB2844", filters={"sektor": "offentlig,privat", "år": "2024"})
```

### Analyze Water Consumption Patterns
```
1. search_tables(query="water", lang="en")
2. get_table_info(table_id="TAB5055")
3. get_table_data(table_id="TAB5055", filters={"sektor": "hushåll,näringsliv,jordbruk", "år": "2024"})
```

### Examine Air Quality Indicators
```
1. search_tables(query="air quality", lang="en")
2. get_table_info(table_id="TAB6489")
3. get_table_data(table_id="TAB6489", filters={"förorening": "NO2,PM10,SO2", "år": "2024"})
```

### Retrieve Sustainability Development Goals Indicators
```
1. search_tables(query="sustainability", lang="en")
2. get_table_info(table_id="TAB5055")
3. get_table_data(table_id="TAB5055", filters={"sdg_mål": "7,11,12,13", "år": "2024"})
```

### Compare Environmental Performance Across Regions
```
1. search_tables(query="climate", lang="en")
2. get_table_info(table_id="TAB5055")
3. get_codelist(codelist_id="Region")
4. get_table_data(table_id="TAB5055", filters={"region": "01,02,03", "år": "2024"})
```