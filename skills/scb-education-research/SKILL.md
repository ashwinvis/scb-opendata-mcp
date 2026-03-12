---
name: scb-education-research
description: Workflows and use cases for SCB Education and Research tables covering schools, universities, and R&D statistics
---

# SCB Education and Research Tables

This skill provides workflows for accessing Statistics Sweden's education and research data, including school statistics, university enrollment, R&D expenditures, innovation metrics, and educational outcomes.

## Common Table IDs and Keywords

- **School Statistics**: TAB2107, TAB372 (keywords: "schools", "skolor", "primary education")
- **University Statistics**: TAB1302, TAB1312 (keywords: "universities", "universitet", "higher education")
- **R&D Statistics**: TAB5798, TAB5794 (keywords: "R&D", "FoU", "research and development")
- **Innovation Statistics**: TAB3780, TAB3775 (keywords: "innovation", "innovation", "business innovation")
- **Adult Education**: TAB325, TAB3834 (keywords: "adult education", "vuxenutbildning", "continuing education")
- **Educational Outcomes**: TAB2107, TAB372 (keywords: "educational outcomes", "utbildningsresultat", "graduation rates")
- **International Students**: TAB1302, TAB1312 (keywords: "international students", "utbytesstudenter", "foreign students")

## Use Cases & Examples

### Retrieve Primary School Statistics
```
1. search_tables(query="schools", lang="en")
2. get_table_info(table_id="TAB2107")
3. get_table_data(table_id="TAB2107", filters={"skoltyp": "grundskola", "år": "2024"})
```

### Analyze University Enrollment Trends
```
1. search_tables(query="universities", lang="en")
2. get_table_info(table_id="TAB1302")
3. get_table_data(table_id="TAB1302", filters={"utbildningsområde": "STEM,humaniora", "år": "2020-2024"})
```

### Examine R&D Expenditures by Sector
```
1. search_tables(query="R&D", lang="en")
2. get_table_info(table_id="TAB5798")
3. get_table_data(table_id="TAB5798", filters={"sektor": "företag,högskola,stat", "år": "2024"})
```

### Retrieve Innovation Statistics for Business Sector
```
1. search_tables(query="innovation", lang="en")
2. get_table_info(table_id="TAB3780")
3. get_table_data(table_id="TAB3780", filters={"näringsgren": "tillverkning,tjänster", "år": "2024"})
```

### Analyze Adult Education Participation
```
1. search_tables(query="adult education", lang="en")
2. get_table_info(table_id="TAB325")
3. get_table_data(table_id="TAB325", filters={"åldersgrupp": "25-44,45-64", "år": "2024"})
```

### Examine Educational Outcomes and Graduation Rates
```
1. search_tables(query="schools", lang="en")
2. get_table_info(table_id="TAB2107")
3. get_table_data(table_id="TAB2107", filters={"utbildningsnivå": "sekundär,tertiär", "år": "2024"})
```

### Retrieve International Student Statistics
```
1. search_tables(query="universities", lang="en")
2. get_table_info(table_id="TAB1302")
3. get_table_data(table_id="TAB1302", filters={"ursprungsland": "EU,icke-EU", "år": "2024"})
```

### Compare Education Performance Across Regions
```
1. search_tables(query="schools", lang="en")
2. get_table_info(table_id="TAB2107")
3. get_codelist(codelist_id="Region")
4. get_table_data(table_id="TAB2107", filters={"region": "01,02,03", "år": "2024"})
```