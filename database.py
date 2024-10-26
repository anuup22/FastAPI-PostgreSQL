from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# this should be in a .env file
URL_DATABASE = "postgresql://myroot:mypassword@localhost:5432/quizapplication"

# engine handles the connection with the database
engine = create_engine(URL_DATABASE)

# SessionLocal handles the transactions with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base handles the models of the database
Base = declarative_base()