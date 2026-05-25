from sqlalchemy import declarative_base
from sqlalchemy import Column, Integer,Date

Base = declarative_base()

class Iscrizioni(Base):
    __tablename__ = "Iscrizioni"

    IscrizioniId = Column(Integer, primary_key=True)
    CorsoId = Column(Integer, foreign_key='Corso.CorsoId')
    StudenteId = Column(Integer, foreign_key='Studenti.StudenteId')
    DataIscrizione = Column(Date)
