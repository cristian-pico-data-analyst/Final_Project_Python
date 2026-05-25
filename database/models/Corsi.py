from sqlalchemy import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class Corsi(Base):
    __tablename__ = "Corsi"

    CorsoId = Column(Integer, primary_key=True)
    NomeCorso = Column(String(50), nullable=False)
    DescrizioneCorso = Column(String(150), nullable=False)
    Crediti = Column(String(50), nullable=False)
    Durata = Column(DateTime, nullable=False)