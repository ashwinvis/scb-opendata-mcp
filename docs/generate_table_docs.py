#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests",
# ]
# ///
"""
Script to generate markdown documentation from SCB table JSON files.
Converts the paginated JSON data into human-readable markdown format.
"""

import json
from pathlib import Path


def load_table_page(page_file):
    """Load a single page of table data from JSON file."""
    with open(page_file, encoding="utf-8") as f:
        return json.load(f)


def generate_table_markdown(table_data, table_index):
    """Generate markdown for a single table."""
    table = table_data

    # Find metadata and data links safely
    metadata_link = None
    data_link = None

    for link in table["links"]:
        if link["rel"] == "metadata":
            metadata_link = link["href"]
        elif link["rel"] == "data":
            data_link = link["href"]

    markdown = f"""
### {table_index}. {table["id"]} - {table["label"]}
- **Period**: {table["firstPeriod"]} to {table["lastPeriod"]}
- **Time Unit**: {table["timeUnit"]}
- **Variables**: {", ".join(table["variableNames"])}
- **Category**: {table["category"]}
- **Subject Code**: {table["subjectCode"]}
- **Last Updated**: {table["updated"]}
- **Source**: {table["source"]}

**API Endpoints:**
- [Metadata]({metadata_link})
- [Data]({data_link})

**Path**: {" → ".join([f"{path['label']} ({path['id']})" for path in table["paths"][0]])}
"""

    return markdown


def process_page(page_file, output_dir):
    """Process a single page file and generate markdown."""
    page_data = load_table_page(page_file)
    page_number = page_data["page"]["pageNumber"]

    # Create output file
    output_file = output_dir / f"page_{page_number}.md"

    with open(output_file, "w", encoding="utf-8") as f:
        # Write header
        f.write(f"# SCB Tables - Page {page_number}\n\n")
        f.write(f"**Total Tables on This Page**: {len(page_data['tables'])}\n\n")
        f.write(
            f"**Page Info**: {page_data['page']['pageNumber']}/{page_data['page']['totalPages']} pages, "
            f"{page_data['page']['totalElements']} total tables\n\n"
        )

        # Write table of contents
        f.write("## Table of Contents\n\n")
        for i, table in enumerate(page_data["tables"], 1):
            table_index = ((page_number - 1) * page_data["page"]["pageSize"]) + i
            f.write(
                f"{table_index}. [{table['id']} - {table['label'][:50]}...](#{table['id'].lower()})\n"
            )

        f.write("\n---\n\n")

        # Write table details
        f.write("## Table Details\n\n")

        for i, table in enumerate(page_data["tables"], 1):
            table_index = ((page_number - 1) * page_data["page"]["pageSize"]) + i
            table_md = generate_table_markdown(table, table_index)
            f.write(table_md)
            f.write("\n---\n\n")

    print(f"Generated {output_file} with {len(page_data['tables'])} tables")


def main():
    # Input and output directories
    input_dir = Path("tables")
    output_dir = Path("tables_docs")
    output_dir.mkdir(exist_ok=True)

    # Process all page files
    page_files = sorted(input_dir.glob("page_*.json"))

    print(f"Found {len(page_files)} page files to process")

    for page_file in page_files:
        print(f"Processing {page_file.name}...")
        process_page(page_file, output_dir)

    print(f"Completed processing {len(page_files)} pages")
    print(f"Markdown files saved to {output_dir}")


if __name__ == "__main__":
    main()
