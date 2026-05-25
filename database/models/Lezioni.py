from sqlalchemy import declarative_base
from sqlalchemy import Column, Integer,Date, String, CHAR, Float, DateTime, ForeignKey

Base = declarative_base()

class Lezioni(Base):
    __tablename__ = "Lezioni"

    LezioneId = Column(Integer, primary_key=True)
    CorsoID = Column(String(50), nullable=False)
    AulaID = Column(String(50), nullable=False)
    DataLezione = Column(Date)
    OraInizio = Column(DateTime)
    OraFine = Column(DateTime)