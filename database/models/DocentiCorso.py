from sqlalchemy import declarative_base
from sqlalchemy import Column, Integer,Date, String, CHAR, Float, DateTime, ForeignKey

Base = declarative_base()

class DocentiCorso(Base):
    __tablename__ = "DocentiCorso"

    Id = Column(Integer, primary_key=True)
    DocenteId = Column(Integer)
    CorsoId = Column(Integer)