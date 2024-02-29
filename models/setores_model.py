from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.database import Base

class Setores(Base):
    __tablename__ = 'setores'

    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String, index = True)
    sigla = Column(String, index = True)
    impressora = Column(String, index = True)