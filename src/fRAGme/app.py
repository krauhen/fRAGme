"""
This module sets up the FastAPI application for the fRAGme service,
which provides a Retrieval Augmented Generation (RAG) Service.
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fRAGme.api.v1.data import router as data_router
from fRAGme.api.v1.cmd import router as cmd_router
from fRAGme.api.v1.auth import router as auth_router
from fRAGme.util.v1.chroma_handler import get_vector_store

# Load environment variables from a .env file
load_dotenv(verbose=True, override=True)

# Initialize the FastAPI app
app = FastAPI(
    title="fRAGme",
    description="Retrieval Augmented Generation (RAG) Service.",
)

# Include the API routers
app.include_router(data_router, prefix="/data/v1", tags=["data"])
app.include_router(cmd_router, prefix="/cmd/v1", tags=["cmd"])

if os.getenv("AUTH", False).lower() in ["true"]:
    app.include_router(auth_router, prefix="", tags=["auth"])
    allow_credentials = True
else:
    allow_credentials = False

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ORIGIN", "*")],
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        get_vector_store("base")
        yield
    except Exception as e:
        raise e
    finally:
        pass


@app.get("/")
def healthcheck():
    """Endpoint for a healthcheck.

    Returns:
        bool: Returns `True` if the webservice is healthy.
    """
    return True
