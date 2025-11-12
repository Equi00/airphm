import pkgutil
import importlib
from fastapi import FastAPI
from databases.sql_database import postgres_engine, PostgresBase
from fastapi.middleware.cors import CORSMiddleware
import entities

for _, module_name, _ in pkgutil.iter_modules(entities.__path__):
    importlib.import_module(f"entities.{module_name}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # allow calls from frontend
    allow_credentials=True,
    allow_methods=["*"], # allow methods (GET, POST, PUT, DELETE)
    allow_headers=["*"] # allow all headers
)

entities.PostgresBase.metadata.create_all(bind=postgres_engine)