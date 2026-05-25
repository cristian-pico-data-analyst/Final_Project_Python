from sqlalchemy import declarative_base
from sqlalchemy import Column, Integer,Date, String, CHAR, Float, DateTime, ForeignKey

Base = declarative_base()

class Iscrizioni(Base):
    __tablename__ = "Iscrizioni"

    IscrizioniId = Column(Integer, primary_key=True)
    CorsoId = Column(Integer, primary_key=True)
    StudenteId = Column(Integer, primary_key=True)
    DataIscrizione = Column(Date)
