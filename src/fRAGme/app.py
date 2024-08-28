import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fRAGme.api.v1.data import router as data_router
from fRAGme.api.v1.cmd import router as cmd_router
from fRAGme.util.v1.chroma_handler import get_vector_store
from dotenv import load_dotenv


load_dotenv()

app = FastAPI(
    title="fRAGme",
    description="Retrieval Augmented Generation (RAG) Service.",
)
app.include_router(data_router, prefix="/data/v1", tags=["data"])
app.include_router(cmd_router, prefix="/cmd/v1", tags=["cmd"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ORIGIN", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def start_app():
    get_vector_store("base")


@app.on_event("shutdown")
def stop_app():
    pass


@app.get("/")
def healthcheck():
    return True
