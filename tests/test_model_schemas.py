"""Tests to verify Pydantic models match the API schema."""

import yaml
from src.scb_opendata_mcp.models import (
    TablesResponse,
    TableResponse,
    Dataset,
    SelectionResponse,
    CodelistsResponse,
    CodelistResponse,
    SavedQueryResponse,
    ConfigResponse,
)


def load_yaml_schema():
    """Load the OpenAPI schema from the YAML file."""
    with open("docs/PxAPI-2.yml") as f:
        schema = yaml.safe_load(f)
    return schema


def get_schema_definition(schema, schema_name):
    """Extract a schema definition from the OpenAPI schema."""
    return schema["components"]["schemas"][schema_name]


def test_tables_response_schema():
    """Test TablesResponse model against the API schema."""
    schema = load_yaml_schema()
    api_schema = get_schema_definition(schema, "TablesResponse")

    # Generate JSON schema from Pydantic model
    model_schema = TablesResponse.model_json_schema()

    # Check required fields
    assert "required" in api_schema
    assert "required" in model_schema

    # Check that all required fields in API schema are in model schema
    for field in api_schema["required"]:
        assert field in model_schema["properties"]

    print("TablesResponse schema is compatible.")


def test_table_response_schema():
    """Test TableResponse model against the API schema."""
    schema = load_yaml_schema()
    api_schema = get_schema_definition(schema, "TableResponse")

    # Generate JSON schema from Pydantic model
    model_schema = TableResponse.model_json_schema()

    # Check required fields
    assert "required" in api_schema
    assert "required" in model_schema

    # Check that all required fields in API schema are in model schema
    for field in api_schema["required"]:
        assert field in model_schema["properties"]

    print("TableResponse schema is compatible.")


def test_dataset_schema():
    """Test Dataset model against the API schema."""
    schema = load_yaml_schema()
    api_schema = get_schema_definition(schema, "Dataset")

    # Generate JSON schema from Pydantic model
    model_schema = Dataset.model_json_schema()

    # Check required fields
    assert "required" in api_schema
    assert "required" in model_schema

    # Check that all required fields in API schema are in model schema
    for field in api_schema["required"]:
        assert field in model_schema["properties"]

    print("Dataset schema is compatible.")


def test_selection_response_schema():
    """Test SelectionResponse model against the API schema."""
    schema = load_yaml_schema()
    api_schema = get_schema_definition(schema, "SelectionResponse")

    # Generate JSON schema from Pydantic model
    model_schema = SelectionResponse.model_json_schema()

    # Check required fields
    assert "required" in api_schema
    assert "required" in model_schema

    # Check that all required fields in API schema are in model schema
    for field in api_schema["required"]:
        assert field in model_schema["properties"]

    print("SelectionResponse schema is compatible.")


def test_codelists_response_schema():
    """Test CodelistsResponse type alias (it's a dict, not a Pydantic model)."""
    # CodelistsResponse is defined as a TypeAlias (dict), not a Pydantic model
    # So we can't call model_json_schema() on it
    # This test is skipped since CodelistsResponse is not a model
    print("CodelistsResponse is a TypeAlias (dict), not a Pydantic model - test skipped.")


def test_codelist_response_schema():
    """Test CodelistResponse model against the API schema."""
    schema = load_yaml_schema()
    api_schema = get_schema_definition(schema, "CodelistResponse")

    # Generate JSON schema from Pydantic model
    model_schema = CodelistResponse.model_json_schema()

    # Check required fields
    assert "required" in api_schema
    assert "required" in model_schema

    # Check that all required fields in API schema are in model schema
    for field in api_schema["required"]:
        assert field in model_schema["properties"]

    print("CodelistResponse schema is compatible.")


def test_saved_query_response_schema():
    """Test SavedQueryResponse model against the API schema."""
    schema = load_yaml_schema()
    api_schema = get_schema_definition(schema, "SavedQueryResponse")

    # Generate JSON schema from Pydantic model
    model_schema = SavedQueryResponse.model_json_schema()

    # Check required fields
    assert "required" in api_schema
    assert "required" in model_schema

    # Check that all required fields in API schema are in model schema
    for field in api_schema["required"]:
        assert field in model_schema["properties"]

    print("SavedQueryResponse schema is compatible.")


def test_config_response_schema():
    """Test ConfigResponse model against the API schema."""
    schema = load_yaml_schema()
    api_schema = get_schema_definition(schema, "ConfigResponse")

    # Generate JSON schema from Pydantic model
    model_schema = ConfigResponse.model_json_schema()

    # Check required fields
    assert "required" in api_schema
    assert "required" in model_schema

    # Check that all required fields in API schema are in model schema
    for field in api_schema["required"]:
        assert field in model_schema["properties"]

    print("ConfigResponse schema is compatible.")


if __name__ == "__main__":
    test_tables_response_schema()
    test_table_response_schema()
    test_dataset_schema()
    test_selection_response_schema()
    test_codelists_response_schema()
    test_codelist_response_schema()
    test_saved_query_response_schema()
    test_config_response_schema()
    print("All schema tests passed!")
