from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from configs.database import Base

class Solicitacoes(Base):
    __tablename__ = 'solicitacoes'

    id = Column(Integer, primary_key= True, index=True)
    nome = Column(String, index=True)
    matricula = Column(String, index=True)
    quantidade_resmas = Column(Integer, index=True)
    id_setor = Column(Integer, ForeignKey("setores.id"))