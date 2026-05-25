from sqlalchemy import declarative_base
from sqlalchemy import Column, Integer

Base = declarative_base()

class DocentiCorso(Base):
    __tablename__ = "DocentiCorso"

    Id = Column(Integer, primary_key=True)
    DocenteId = Column(Integer, foreign_key="Docenti.DocentiId")
    CorsoId = Column(Integer, foreign_key="Corso.CorsoId")