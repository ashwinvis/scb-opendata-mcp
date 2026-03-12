---
name: scb-living-conditions
description: Workflows and use cases for SCB Living Conditions tables covering income, education, health, and social statistics
---

# SCB Living Conditions Tables

This skill provides workflows for accessing Statistics Sweden's living conditions data, including income distribution, education levels, health statistics, gender equality, IT usage, and various social indicators.

## Common Table IDs and Keywords

- **Income Statistics**: TAB6240, TAB6241, TAB6243 (keywords: "income", "inkomst", "income distribution")
- **Education Levels**: TAB4500, TAB6244 (keywords: "education", "utbildning", "education levels")
- **Health Statistics**: TAB6489, TAB6490, TAB6491 (keywords: "health", "hälsa", "health indicators")
- **Gender Equality**: TAB5629 (keywords: "gender equality", "jämställdhet", "equality statistics")
- **IT Usage**: TAB4672, TAB4673 (keywords: "IT usage", "IT-användning", "digital divide")
- **Child and Family**: TAB4503, TAB2691, TAB2700 (keywords: "children", "families", "barn och familj")
- **Poverty Indicators**: TAB6240, TAB6241 (keywords: "poverty", "fattigdom", "social exclusion")

## Use Cases & Examples

### Retrieve Income Distribution Statistics
```
1. search_tables(query="income", lang="en")
2. get_table_info(table_id="TAB6240")
3. get_table_data(table_id="TAB6240", filters={"inkomstgrupp": "låg,medel,hög", "år": "2024"})
```

### Analyze Education Levels by Region
```
1. search_tables(query="education", lang="en")
2. get_table_info(table_id="TAB4500")
3. get_table_data(table_id="TAB4500", filters={"region": "01", "utbildningsnivå": "grund,sekundär,tertiär", "år": "2024"})
```

### Examine Health Indicators and Life Expectancy
```
1. search_tables(query="health", lang="en")
2. get_table_info(table_id="TAB6489")
3. get_table_data(table_id="TAB6489", filters={"kön": "1,2", "åldersgrupp": "alla", "år": "2024"})
```

### Retrieve Gender Equality Statistics
```
1. search_tables(query="gender equality", lang="en")
2. get_table_info(table_id="TAB5629")
3. get_table_data(table_id="TAB5629", filters={"område": "utbildning,sysselsättning,inkomst", "år": "2024"})
```

### Analyze IT Usage and Digital Divide
```
1. search_tables(query="IT usage", lang="en")
2. get_table_info(table_id="TAB4672")
3. get_table_data(table_id="TAB4672", filters={"åldersgrupp": "16-24,25-64,65+", "år": "2024"})
```

### Examine Child and Family Statistics
```
1. search_tables(query="children", lang="en")
2. get_table_info(table_id="TAB4503")
3. get_table_data(table_id="TAB4503", filters={"familjetyp": "ensam,ensam_med_barn", "år": "2024"})
```

### Analyze Poverty and Social Exclusion Indicators
```
1. search_tables(query="poverty", lang="en")
2. get_table_info(table_id="TAB6240")
3. get_table_data(table_id="TAB6240", filters={"fattigdomsindikator": "låg_inkomst,material_deprivation", "år": "2024"})
```

### Compare Living Conditions Across Regions
```
1. search_tables(query="income", lang="en")
2. get_table_info(table_id="TAB6240")
3. get_codelist(codelist_id="Region")
4. get_table_data(table_id="TAB6240", filters={"region": "01,02,03", "år": "2024"})
```