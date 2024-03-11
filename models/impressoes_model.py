from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from configs.database import Base


class Impressoes(Base):
    __tablename__ = 'impressoes'

    id = Column(Integer, primary_key= True, index=True)
    quantidade_impressoes = Column(Integer, index=True)
    id_setor = Column(Integer, ForeignKey("setores.id"))