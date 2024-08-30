"""
This module sets up the FastAPI application for the fRAGme service,
which provides a Retrieval Augmented Generation (RAG) Service.
"""

import os

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fRAGme.api.v1.data import router as data_router
from fRAGme.api.v1.cmd import router as cmd_router
from fRAGme.util.v1.chroma_handler import get_vector_store

# Load environment variables from a .env file
load_dotenv(verbose=True, override=False)


# Initialize the FastAPI app
app = FastAPI(
    title="fRAGme",
    description="Retrieval Augmented Generation (RAG) Service.",
)

# Include the API routers
app.include_router(data_router, prefix="/data/v1", tags=["data"])
app.include_router(cmd_router, prefix="/cmd/v1", tags=["cmd"])

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ORIGIN", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def start_app():
    """Event handler for the startup event.

    Initializes the vector store when the application starts.
    """
    get_vector_store("base")


@app.on_event("shutdown")
def stop_app():
    """Event handler for the shutdown event.

    This function is called when the application is shutting down.
    Currently, it does nothing but can be used for cleanup tasks.
    """
    return


@app.get("/")
def healthcheck():
    """Endpoint for a healthcheck.

    Returns:
        bool: Returns `True` if the webservice is healthy.
    """
    return True
