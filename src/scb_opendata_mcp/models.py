from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class TablesResponse(BaseModel):
    language: str
    tables: List[Dict[str, Any]]
    page: Dict[str, Any]
    links: Optional[List[Dict[str, Any]]] = None

class TableResponse(BaseModel):
    language: str
    id: str
    label: Optional[str] = None
    description: Optional[str] = None
    updated: Optional[str] = None
    firstPeriod: Optional[str] = None
    lastPeriod: Optional[str] = None
    variableNames: List[str]
    discontinued: Optional[bool] = None
    source: Optional[str] = None
    subjectCode: Optional[str] = None
    timeUnit: Optional[str] = None
    paths: Optional[List[List[Dict[str, Any]]]] = None
    links: Optional[List[Dict[str, Any]]] = None

class Dataset(BaseModel):
    version: str
    class_: str = Field(alias="class")
    href: Optional[str] = None
    label: Optional[str] = None
    source: Optional[str] = None
    updated: Optional[str] = None
    link: Optional[Dict[str, Any]] = None
    note: Optional[List[str]] = None
    role: Optional[Dict[str, Any]] = None
    id: List[str]
    size: List[int]
    dimension: Dict[str, Any]
    extension: Optional[Dict[str, Any]] = None
    value: Optional[List[Any]] = None
    status: Optional[Dict[str, str]] = None

class SelectionResponse(BaseModel):
    selection: List[Dict[str, Any]]
    placement: Optional[Dict[str, Any]] = None
    language: str
    links: List[Dict[str, Any]]

class CodelistsResponse(BaseModel):
    language: str
    codelists: List[Dict[str, Any]]
    links: Optional[List[Dict[str, Any]]] = None

class CodelistResponse(BaseModel):
    id: str
    label: str
    language: str
    languages: List[str]
    elimination: Optional[bool] = None
    eliminationValueCode: Optional[str] = None
    type: str
    values: List[Dict[str, Any]]
    links: List[Dict[str, Any]]

class SavedQueryResponse(BaseModel):
    language: str
    id: str
    savedQuery: Dict[str, Any]
    links: List[Dict[str, Any]]

class ConfigResponse(BaseModel):
    apiVersion: str
    appVersion: str
    languages: List[Dict[str, Any]]
    defaultLanguage: str
    maxDataCells: int
    maxCallsPerTimeWindow: int
    timeWindow: int
    license: str
    defaultDataFormat: str
    dataFormats: List[str]
    features: Optional[List[Dict[str, Any]]] = None
    sourceReferences: Optional[List[Dict[str, Any]]] = None
