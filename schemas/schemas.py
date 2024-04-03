from pydantic import BaseModel
from fastapi import Form

class SetoresResponse(BaseModel):
    id: int
    nome: str
    sigla: str
    impressora: str

class SetoresRequest(BaseModel):
    nome: str
    sigla: str
    impressora: str

class SolicitacoesResponse(BaseModel):
    id: int
    nome: str
    matricula: str
    quantidade_resmas: int
    id_setor: int

class SolicitacoesRequest(BaseModel):
    nome: str
    matricula: str
    quantidade_resmas: int
    id_setor: int

class ImpressoesResponse(BaseModel):
    id: int
    quantidade_impressoes: int
    id_setor: int

class ImpressoesRequest(BaseModel):
    quantidade_impressoes: int
    id_setor: int