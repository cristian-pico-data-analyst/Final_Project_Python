from sqlalchemy import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Docenti(Base):
    __tablename__ = "Docenti"

    DocenteId = Column(Integer, primary_key=True)
    Nome = Column(String(50), nullable=False)
    Cognome = Column(String(50), nullable=False)
    Email = Column(String(50), unique=True)
    Specializzazione = Column(String(50), nullable=False)
