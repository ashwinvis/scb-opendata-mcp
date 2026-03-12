---
name: scb-international-trade
description: Workflows and use cases for SCB International Trade tables covering imports, exports, and foreign trade statistics
---

# SCB International Trade Tables

This skill provides workflows for accessing Statistics Sweden's international trade data, including import/export statistics, trade balances, commodity flows, and foreign trade indicators.

## Common Table IDs and Keywords

- **Import Statistics**: TAB5440, TAB1630, TAB1631 (keywords: "imports", "import", "import statistics")
- **Export Statistics**: TAB5440, TAB1630, TAB1631 (keywords: "exports", "export", "export statistics")
- **Trade Balance**: TAB5440 (keywords: "trade balance", "handelsbalans", "net trade")
- **Commodity Trade**: TAB1630, TAB1631 (keywords: "commodity trade", "varuhandel", "goods trade")
- **Service Trade**: TAB6695, TAB6696 (keywords: "service trade", "tjänstehandel", "services trade")
- **Foreign Direct Investment**: TAB2844, TAB2843 (keywords: "FDI", "foreign investment", "utländska investeringar")
- **Trade by Country**: TAB5440 (keywords: "trade by country", "handel per land", "country-specific trade")

## Use Cases & Examples

### Retrieve Current Import Statistics
```
1. search_tables(query="imports", lang="en")
2. get_table_info(table_id="TAB5440")
3. get_table_data(table_id="TAB5440", filters={"varugrupp": "maskiner,kemikalier", "år": "2024"})
```

### Analyze Export Trends by Commodity
```
1. search_tables(query="exports", lang="en")
2. get_table_info(table_id="TAB5440")
3. get_table_data(table_id="TAB5440", filters={"vara": "trä,stål,fordon", "år": "2020-2024"})
```

### Examine Trade Balance Statistics
```
1. search_tables(query="trade balance", lang="en")
2. get_table_info(table_id="TAB5440")
3. get_table_data(table_id="TAB5440", filters={"sektor": "total", "år": "2024", "kvartal": "K1-K4"})
```

### Retrieve Commodity-Specific Trade Data
```
1. search_tables(query="commodity trade", lang="en")
2. get_table_info(table_id="TAB1630")
3. get_table_data(table_id="TAB1630", filters={"vara": "elektronik", "handelstyp": "import,export", "år": "2024"})
```

### Analyze Service Trade Patterns
```
1. search_tables(query="service trade", lang="en")
2. get_table_info(table_id="TAB6695")
3. get_table_data(table_id="TAB6695", filters={"tjänstetyp": "transport,finansiell,turism", "år": "2024"})
```

### Examine Foreign Direct Investment Flows
```
1. search_tables(query="foreign investment", lang="en")
2. get_table_info(table_id="TAB2844")
3. get_table_data(table_id="TAB2844", filters={"investeringstyp": "inflöde,utflöde", "år": "2024"})
```

### Retrieve Country-Specific Trade Statistics
```
1. search_tables(query="trade by country", lang="en")
2. get_table_info(table_id="TAB5440")
3. get_table_data(table_id="TAB5440", filters={"land": "DE,US,CN", "handelstyp": "export", "år": "2024"})
```

### Compare Trade Performance Across Commodity Groups
```
1. search_tables(query="imports", lang="en")
2. get_table_info(table_id="TAB5440")
3. get_codelist(codelist_id="Varugrupp")
4. get_table_data(table_id="TAB5440", filters={"varugrupp": "jordbruk,tillverkning", "år": "2024"})
```