from sqlalchemy import declarative_base
from sqlalchemy import Column, Integer,Date, String, CHAR, Float, DateTime, ForeignKey

Base = declarative_base()

class Aule(Base):
    __tablename__ = "Aule"

    AulaId = Column(Integer, primary_key=True)
    NomeAula = Column(String(50), nullable=False)
    Capacita = Column(String(50), nullable=False)