from fastapi import APIRouter, HTTPException, File, UploadFile
from fRAGme.util.v1.chroma_handler import *

router = APIRouter()


@router.post("/add_texts")
def data_add_text(texts: List[Text], identifier: str):
    try:
        add_texts(texts, identifier)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"result": True}


@router.post("/add_pdfs")
def data_add_pdfs(identifier: str, pdfs: List[UploadFile] = File(...)):
    try:
        add_pdfs(identifier, pdfs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"result": True}


@router.post("/get_texts")
def data_get_texts(identifier: str, ids: List[str]):
    try:
        documents = get_texts(identifier, ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"result": documents}


@router.get("/get_pdfs")
def data_get_pdfs(identifier: str):
    try:
        documents = get_pdfs(identifier)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"result": documents}


@router.get("/get_databases")
def data_get_databases():
    try:
        documents = get_databases()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"result": documents}


@router.put("/update_texts")
def data_update_texts(identifier: str, updates: Dict[str, TextUpdate]):
    try:
        update_texts(identifier, updates)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"result": True}


@router.delete("/delete_texts")
def data_delete_texts(identifier: str, ids: List[str]):
    try:
        delete_texts(identifier, ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"result": True}


@router.delete("/delete_pdfs")
def data_delete_pdfs(identifier: str, pdf_names: List[str]):
    try:
        delete_pdfs(identifier, pdf_names)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"result": True}


@router.delete("/delete_databases")
def data_delete_databases(identifiers: List[str]):
    try:
        delete_databases(identifiers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"result": True}
