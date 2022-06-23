from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# "connecting" to a SQLite database (opening a file with the SQLite database)
# The file will be located at the same directory in the file adress.db
SQLALCHEMY_DATABASE_URL="sqlite:///./adress.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# I name it SessionLocal to distinguish it from the Session and importing from SQLAlchemy.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()