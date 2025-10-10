from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# For docker image excecution
#URL_DATABASE_POSTGRES = "postgresql://postgres:postgres@db:5432/AirphmApp"

# For local excecution
URL_DATABASE_POSTGRES = "postgresql//postgres:postgres@localhost:5432/AirphmApp"

postgres_engine = create_engine(URL_DATABASE_POSTGRES)

PostgresSessionLocal = sessionmaker(autoflush=False, bind=postgres_engine)

PostgresBase = declarative_base()