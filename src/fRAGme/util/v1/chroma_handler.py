import glob
import os
import shutil

from typing import List
from uuid import uuid4
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from fRAGme.models.v1.data import *
from fRAGme.models.v1.cmd import *

vector_stores = dict()


def create_vector_store(identifier):
    data_path = os.getenv("DATA_PATH")
    filename = os.path.join(data_path, f"{identifier}_chroma_langchain_db")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = Chroma(
        collection_name=identifier,
        embedding_function=embeddings,
        persist_directory=filename,
    )
    return vector_store


def get_vector_store(identifier):
    if identifier not in vector_stores.keys() or vector_stores[identifier] is None:
        vector_store = create_vector_store(identifier)
        vector_stores[identifier] = vector_store
    else:
        vector_store = vector_stores[identifier]
    return vector_store


def add_texts(texts: List[Text], identifier: str):
    documents = list()
    for element in texts:
        document = Document(
            page_content=element.text,
            metadata=element.metadata,
        )
        documents.append(document)
    uuids = [str(uuid4()) for _ in range(len(documents))]

    vector_store = get_vector_store(identifier)
    vector_store.add_documents(documents=documents, ids=uuids)


def add_pdfs(identifier: str, pdfs):
    documents = list()
    for pdf in pdfs:
        file_path = os.path.join("/tmp", pdf.filename)
        with open(file_path, "wb") as f:
            f.write(pdf.file.read())

        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        os.remove(file_path)

        documents.extend(pages)

    if len(documents) > 0:
        uuids = [str(uuid4()) for _ in range(len(documents))]

        vector_store = get_vector_store(identifier)
        vector_store.add_documents(documents=documents, ids=uuids)
    else:
        raise Exception("PDF has no text pages.(Maybe all pages are images?!)")


def get_texts(identifier: str, ids: List[str] = None):
    vector_store = get_vector_store(identifier)
    if ids is not None:
        documents = vector_store.get(ids=ids)
    else:
        documents = vector_store.get()

    elements = dict()
    for id_, text, metadata in zip(
        documents["ids"], documents["documents"], documents["metadatas"]
    ):
        elements[id_] = dict()
        elements[id_]["text"] = text
        elements[id_]["metadata"] = metadata

    return elements


def get_pdfs(identifier: str):
    documents = get_texts(identifier)
    filenames = list()
    for id_, element in documents.items():
        if "source" in element["metadata"].keys():
            source = element["metadata"]["source"]
            filename = source.split("/")[-1]
            extension = filename.split(".")[-1]
            if extension == "pdf":
                filenames.append(filename)
    filenames = list(set(filenames))
    return filenames


def get_databases():
    data_path = os.getenv("DATA_PATH")
    databases = glob.glob(os.path.join(data_path, "*_chroma_langchain_db"))
    databases = [
        database.split("/")[-1].replace("_chroma_langchain_db", "")
        for database in databases
    ]
    return databases


def update_texts(identifier: str, updates: Dict[str, TextUpdate]):
    vector_store = get_vector_store(identifier)
    ids = list(updates.keys())
    documents = vector_store.get(ids=ids)
    for id_, metadata in zip(documents["ids"], documents["metadatas"]):
        document = Document(
            page_content=updates[id_].new_text,
            metadata=updates[id_].new_metadata,
        )
        vector_store.update_document(id_, document)


def delete_texts(identifier: str, ids: List[str]):
    vector_store = get_vector_store(identifier)
    vector_store.delete(ids)


def delete_pdfs(identifier: str, pdf_names: List[str]):
    documents = get_texts(identifier)
    ids = list()
    for pdf_name in pdf_names:
        for id_, element in documents.items():
            if "source" in element["metadata"].keys():
                source = element["metadata"]["source"]
                filename = source.split("/")[-1]
                if pdf_name in filename:
                    ids.append(id_)
    ids = list(set(ids))
    if len(ids) > 0:
        delete_texts(identifier, ids)


def delete_databases(identifiers: List[str]):
    for identifier in identifiers:
        data_path = os.getenv("DATA_PATH")
        filepath = os.path.join(data_path, f"{identifier}_chroma_langchain_db")
        if os.path.isdir(filepath):
            vector_stores[identifier] = None
            shutil.rmtree(filepath)


def build_question(data: Question, identifier: str):
    # Add question
    template = f"Question:\n{data.question}\n\n"

    # Add k snippets
    template += f"Info-Snippets:\n"
    vector_store = get_vector_store(identifier)
    snippets = vector_store.similarity_search(
        data.question, k=data.k_similar_text_snippets
    )
    for snippet in snippets:
        template += f"Text: {snippet.page_content}\n"
        template += f"Metadata: {snippet.metadata}"
        template += f"\n\n"

    return template
