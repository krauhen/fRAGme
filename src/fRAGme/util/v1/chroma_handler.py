"""
This module provides utility functions to handle vector stores using Chroma.
"""

import glob
import os
import shutil
import time
from typing import List, Dict
from uuid import uuid4
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

from fRAGme.models.v1.cmd import Question
from fRAGme.models.v1.data import (
    Text,
    TextUpdate,
)

vector_stores = {}


def create_vector_store(identifier: str) -> Chroma:
    """
    Create a vector store for a given identifier.
    """
    data_path = os.getenv("DATA_PATH")
    filename = os.path.join(data_path, f"{identifier}_chroma_langchain_db")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = Chroma(
        collection_name=identifier,
        embedding_function=embeddings,
        persist_directory=filename,
    )
    return vector_store


def get_vector_store(identifier: str) -> Chroma:
    """
    Retrieve the vector store for a given identifier, creating it if necessary.
    """
    if identifier not in vector_stores or vector_stores[identifier] is None:
        vector_store = create_vector_store(identifier)
        vector_stores[identifier] = vector_store
    else:
        vector_store = vector_stores[identifier]
    return vector_store


def add_texts(texts: List[Text], identifier: str):
    """
    Add texts to the vector store for a given identifier.
    """
    documents = []
    for element in texts:
        element.metadata["time_of_creation"] = time.time()
        document = Document(
            page_content=element.text,
            metadata=element.metadata,
        )
        documents.append(document)
    uuids = [str(uuid4()) for _ in range(len(documents))]

    vector_store = get_vector_store(identifier)
    vector_store.add_documents(documents=documents, ids=uuids)


def add_pdfs(identifier: str, pdfs: List):
    """
    Add PDFs to the vector store for a given identifier.
    """
    documents = []
    for pdf in pdfs:
        file_path = os.path.join("/tmp", pdf.filename)
        with open(file_path, "wb") as f:
            f.write(pdf.file.read())

        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        os.remove(file_path)

        documents.extend(pages)

    if documents:
        uuids = [str(uuid4()) for _ in range(len(documents))]

        vector_store = get_vector_store(identifier)
        vector_store.add_documents(documents=documents, ids=uuids)
    else:
        raise ValueError("PDF has no text pages. (Maybe all pages are images?!)")


def get_texts(identifier: str, ids: List[str] = None) -> Dict[str, Text]:
    """
    Retrieve texts from the vector store for a given identifier.
    """
    vector_store = get_vector_store(identifier)
    documents = vector_store.get(ids=ids) if ids else vector_store.get()

    elements = {}
    for id_, text, metadata in zip(
        documents["ids"], documents["documents"], documents["metadatas"]
    ):
        elements[id_] = Text(text=text, metadata=metadata)

    return elements


def get_pdfs(identifier: str) -> List[str]:
    """
    Retrieve PDF filenames from the vector store for a given identifier.
    """
    documents = get_texts(identifier)
    filenames = []
    for element in documents.values():
        if "source" in element.metadata:
            source = element.metadata["source"]
            filename = source.split("/")[-1]
            extension = filename.split(".")[-1]
            if extension == "pdf":
                filenames.append(filename)
    return list(set(filenames))


def get_databases() -> List[str]:
    """
    Retrieve all database identifiers.
    """
    data_path = os.getenv("DATA_PATH")
    databases = glob.glob(os.path.join(data_path, "*_chroma_langchain_db"))
    return [
        database.split("/")[-1].replace("_chroma_langchain_db", "")
        for database in databases
    ]


def update_texts(identifier: str, updates: Dict[str, TextUpdate]):
    """
    Update texts in the vector store for a given identifier.
    """
    vector_store = get_vector_store(identifier)
    ids = list(updates.keys())
    documents = vector_store.get(ids=ids)
    for id_ in documents["ids"]:
        updates[id_].new_metadata["time_of_creation"] = time.time()
        document = Document(
            page_content=updates[id_].new_text,
            metadata=updates[id_].new_metadata,
        )
        vector_store.update_document(id_, document)


def delete_texts(identifier: str, ids: List[str]):
    """
    Delete texts from the vector store for a given identifier.
    """
    vector_store = get_vector_store(identifier)
    vector_store.delete(ids)


def delete_pdfs(identifier: str, pdf_names: List[str]):
    """
    Delete PDFs from the vector store for a given identifier.
    """
    documents = get_texts(identifier)
    ids = []
    for pdf_name in pdf_names:
        for id_, element in documents.items():
            if "source" in element.metadata:
                source = element.metadata["source"]
                filename = source.split("/")[-1]
                if pdf_name in filename:
                    ids.append(id_)
    if ids:
        delete_texts(identifier, list(set(ids)))


def delete_databases(identifiers: List[str]):
    """
    Delete databases for given identifiers.
    """
    for identifier in identifiers:
        data_path = os.getenv("DATA_PATH")
        filepath = os.path.join(data_path, f"{identifier}_chroma_langchain_db")
        if os.path.isdir(filepath):
            vector_stores[identifier] = None
            shutil.rmtree(filepath)


def build_question(data: Question, identifier: str) -> str:
    """
    Build a question template with snippets from the vector store.
    """
    # Add question
    template = f"Question:\n{data.question}\n\n"

    # Add k snippets
    template += "Info-Snippets:\n"
    vector_store = get_vector_store(identifier)
    snippets = vector_store.similarity_search(
        data.question, k=data.k_similar_text_snippets
    )
    for snippet in snippets:
        template += f"Text: {snippet.page_content}\n"
        template += f"Metadata: {snippet.metadata}\n\n"

    return template
