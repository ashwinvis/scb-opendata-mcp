from pydantic import BaseModel, Field
from typing import TypeAlias, Any


class TablesResponse(BaseModel):
    language: str
    tables: list[dict[str, Any]]
    page: dict[str, Any]
    links: list[dict[str, Any]] | None = None


class TableResponse(BaseModel):
    language: str
    id: str
    label: str | None = None
    description: str | None = None
    updated: str | None = None
    firstPeriod: str | None = None
    lastPeriod: str | None = None
    variableNames: list[str]
    discontinued: bool | None = None
    source: str | None = None
    subjectCode: str | None = None
    timeUnit: str | None = None
    paths: list[list[dict[str, Any]]] | None = None
    links: list[dict[str, Any]] | None = None


class Dataset(BaseModel):
    version: str
    class_: str = Field(alias="class")
    href: str | None = None
    label: str | None = None
    source: str | None = None
    updated: str | None = None
    link: dict[str, Any] | None = None
    note: list[str] | None = None
    role: dict[str, Any] | None = None
    id: list[str]
    size: list[int]
    dimension: dict[str, Any]
    extension: dict[str, Any] | None = None
    value: list[Any] | None = None
    status: dict[str, str] | None = None


class SelectionResponse(BaseModel):
    selection: list[dict[str, Any]]
    placement: dict[str, Any] | None = None
    language: str | None = None
    links: list[dict[str, Any]]


CodelistsResponse: TypeAlias = dict[str, list[dict[str, Any]]]


class CodelistResponse(BaseModel):
    id: str
    label: str
    language: str
    languages: list[str]
    elimination: bool | None = None
    eliminationValueCode: str | None = None
    type: str
    values: list[dict[str, Any]]
    links: list[dict[str, Any]]


class SavedQueryResponse(BaseModel):
    language: str
    id: str
    savedQuery: dict[str, Any]
    links: list[dict[str, Any]]


class ConfigResponse(BaseModel):
    apiVersion: str
    appVersion: str
    languages: list[dict[str, Any]]
    defaultLanguage: str
    maxDataCells: int
    maxCallsPerTimeWindow: int
    timeWindow: int
    license: str
    defaultDataFormat: str
    dataFormats: list[str]
    features: list[dict[str, Any]] | None = None
    sourceReferences: list[dict[str, Any]] | None = None
