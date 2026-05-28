from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from app.config import Config

# Create the database engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Setup a scoped database session
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# Base class for declarative models
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """Import models and create schema if not exists."""

    Base.metadata.create_all(bind=engine)
