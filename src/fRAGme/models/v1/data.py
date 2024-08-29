"""
This module contains Pydantic models for handling data requests and responses
related to texts and PDFs in the fRAGme application.
"""

from typing import Dict, Any, List
from pydantic import BaseModel


class Text(BaseModel):
    """
    Model representing a text entry with associated metadata.
    """

    text: str
    metadata: Dict[str, Any] = {"source": "text input"}


class TextUpdate(BaseModel):
    """
    Model representing an update to a text entry.
    """

    new_text: str
    new_metadata: Dict[str, Any]


class DataAddTextsRequest(BaseModel):
    """
    Request model for adding multiple text entries.
    """

    texts: List[Text]
    identifier: str


class DataAddTextsResponse(BaseModel):
    """
    Response model indicating the status of adding text entries.
    """

    status: bool = False


class DataAddPDFsResponse(BaseModel):
    """
    Response model indicating the status of adding PDF entries.
    """

    status: bool = False


class DataGetTextsRequest(BaseModel):
    """
    Request model for retrieving specific text entries by their IDs.
    """

    identifier: str
    ids: List[str] = None


class DataGetTextsResponse(BaseModel):
    """
    Response model containing the requested text entries.
    """

    documents: Dict[str, Text]


class DataGetPDFsRequest(BaseModel):
    """
    Request model for retrieving PDFs associated with an identifier.
    """

    identifier: str


class DataGetPDFsResponse(BaseModel):
    """
    Response model containing the requested PDF names.
    """

    documents: List[str]


class DataGetDatabasesResponse(BaseModel):
    """
    Response model containing the list of available databases.
    """

    databases: List[str]


class DataUploadTextsRequest(BaseModel):
    """
    Request model for uploading updates to text entries.
    """

    identifier: str
    updates: Dict[str, TextUpdate]


class DataUploadTextsResponse(BaseModel):
    """
    Response model indicating the status of uploading text updates.
    """

    status: bool = False


class DataDeleteTextsRequest(BaseModel):
    """
    Request model for deleting specific text entries by their IDs.
    """

    identifier: str
    ids: List[str]


class DataDeleteTextsResponse(BaseModel):
    """
    Response model indicating the status of deleting text entries.
    """

    status: bool = False


class DataDeletePDFsRequest(BaseModel):
    """
    Request model for deleting specific PDFs by their names.
    """

    identifier: str
    pdf_names: List[str]


class DataDeletePDFsResponse(BaseModel):
    """
    Response model indicating the status of deleting PDF entries.
    """

    status: bool = False


class DataDeleteDatabasesRequest(BaseModel):
    """
    Request model for deleting specific databases by their identifiers.
    """

    identifiers: List[str]


class DataDeleteDatabasesResponse(BaseModel):
    """
    Response model indicating the status of deleting databases.
    """

    status: bool = False
