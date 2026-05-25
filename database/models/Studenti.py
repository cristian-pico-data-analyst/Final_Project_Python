from sqlalchemy import declarative_base
from sqlalchemy import Column, Integer,Date, String, CHAR, Float, DateTime, ForeignKey

Base = declarative_base()

class Studenti(Base):
    __tablename__ = "Studenti"

    StudenteId = Column(Integer, primary_key=True)
    Nome = Column(String(50), nullable=False)
    Cognome = Column(String(50), nullable=False)
    DataNascita = Column(Date)
    Email = Column(String(50), unique=True)
    Telefono = Column(String(50), unique=True)
    CodiceFiscale = Column(CHAR(16), unique=True)