"""
This module provides API endpoints for managing text snippets and PDFs in a vector store.
"""

from typing import List, Annotated
from fastapi import APIRouter, HTTPException, File, UploadFile, Depends

from fRAGme.models.v1.auth import User
from fRAGme.util.v1.auth import get_current_active_user
from fRAGme.util.v1.chroma_handler import (
    add_texts,
    add_pdfs,
    get_texts,
    get_pdfs,
    get_databases,
    update_texts,
    delete_texts,
    delete_pdfs,
    delete_databases,
)
from fRAGme.models.v1.data import (
    DataAddTextsRequest,
    DataAddTextsResponse,
    DataAddPDFsResponse,
    DataGetTextsRequest,
    DataGetTextsResponse,
    DataGetPDFsRequest,
    DataGetPDFsResponse,
    DataGetDatabasesResponse,
    DataUploadTextsRequest,
    DataUploadTextsResponse,
    DataDeleteTextsRequest,
    DataDeleteTextsResponse,
    DataDeletePDFsRequest,
    DataDeletePDFsResponse,
    DataDeleteDatabasesRequest,
    DataDeleteDatabasesResponse,
)

router = APIRouter()


@router.post("/add_texts", response_model=DataAddTextsResponse)
def data_add_texts(
    request: DataAddTextsRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Endpoint to add text snippets to a vector store.

    Args:
        request: An request object to fill with parameters.

    Returns:
        Return true if the process was successful.

    Raises:
        HTTPException: Generic internal server error.
    """
    try:
        add_texts(request.texts, request.identifier)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return DataAddTextsResponse(status=True)


@router.post("/add_pdfs", response_model=DataAddPDFsResponse)
def data_add_pdfs(
    identifier: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    pdfs: List[UploadFile] = File(...),
):
    """Endpoint to add pdfs to a vector store.

    Args:
        identifier: Name of the vector store.
        pdfs: PDF objects to upload.

    Returns:
        Return true if the process was successful.

    Raises:
        HTTPException: Generic internal server error.
    """
    try:
        add_pdfs(identifier, pdfs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return DataAddPDFsResponse(status=True)


@router.post("/get_texts", response_model=DataGetTextsResponse)
def data_get_texts(
    request: DataGetTextsRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Endpoint to get text snippets from specified vector store.

    Args:
        request: An request object to fill with parameters.

    Returns:
        Return dictionary of Text objects.

    Raises:
        HTTPException: Generic internal server error.
    """
    try:
        documents = get_texts(request.identifier, request.ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return DataGetTextsResponse(documents=documents)


@router.post("/get_pdfs", response_model=DataGetPDFsResponse)
def data_get_pdfs(
    request: DataGetPDFsRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Endpoint to get pdf name from specified vector store.

    Args:
        request: An request object to fill with parameters.

    Returns:
        Return a list with pdf filenames.

    Raises:
        HTTPException: Generic internal server error.
    """
    try:
        documents = get_pdfs(request.identifier)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return DataGetPDFsResponse(documents=documents)


@router.get("/get_databases", response_model=DataGetDatabasesResponse)
def data_get_databases(current_user: Annotated[User, Depends(get_current_active_user)]):
    """Endpoint to get all present database names.

    Args:

    Returns:
        Return a list with database names.

    Raises:
        HTTPException: Generic internal server error.
    """
    try:
        databases = get_databases()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return DataGetDatabasesResponse(databases=databases)


@router.put("/update_texts", response_model=DataUploadTextsResponse)
def data_update_texts(
    request: DataUploadTextsRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Endpoint to update text snippets.

    Args:
        request: An request object to fill with parameters.

    Returns:
        Return true if the process was successful.

    Raises:
        HTTPException: Generic internal server error.
    """
    try:
        update_texts(request.identifier, request.updates)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return DataUploadTextsResponse(status=True)


@router.delete("/delete_texts", response_model=DataDeleteTextsResponse)
def data_delete_texts(
    request: DataDeleteTextsRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Endpoint to delete text snippets.

    Args:
        request: An request object to fill with parameters.

    Returns:
        Return true if the process was successful.

    Raises:
        HTTPException: Generic internal server error.
    """
    try:
        delete_texts(request.identifier, request.ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return DataDeleteTextsResponse(status=True)


@router.delete("/delete_pdfs", response_model=DataDeletePDFsResponse)
def data_delete_pdfs(
    request: DataDeletePDFsRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Endpoint to delete all text snippets from the specified pdfs.

    Args:
        request: An request object to fill with parameters.

    Returns:
        Return true if the process was successful.

    Raises:
        HTTPException: Generic internal server error.
    """
    try:
        delete_pdfs(request.identifier, request.pdf_names)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return DataDeletePDFsResponse(status=True)


@router.delete("/delete_databases", response_model=DataDeleteDatabasesResponse)
def data_delete_databases(
    request: DataDeleteDatabasesRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Endpoint to delete all databases.

    Args:
        request: An request object to fill with parameters.

    Returns:
        Return true if the process was successful.

    Raises:
        HTTPException: Generic internal server error.
    """
    try:
        delete_databases(request.identifiers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return DataDeleteDatabasesResponse(status=True)
