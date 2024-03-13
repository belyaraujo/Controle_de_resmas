from fastapi import Depends, Request
from fastapi.routing import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel, Field, validator
from pytest import Session
from typing import List

from configs.dependencies import get_db
from configs.templates_config import TEMPLATES, MEDIA

from models.solicitacoes_model import Solicitacoes
from models.setores_model import Setores
from models.impressoes_model import Impressoes



router = APIRouter()

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

    class Config:
        orm_mode = True

class SolicitacoesRequest(BaseModel):
    nome: str 
    matricula: str 
    quantidade_resmas: int = Field(gt=0)
    id_setor: int


class ImpressoesResponse(BaseModel):
    id: int
    quantidade_impressoes: int
    id_setor: int

class ImpressoesRequest(BaseModel):
    quantidade_impressoes: int
    id_setor: int


# @router.get('/', response_model=List[SetoresResponse])
# def listar_setores(db: Session = Depends(get_db)) -> List[SetoresResponse]:
#     setores = db.query(Setores).all()
#     return setores

@router.get('/solicitacao', response_model=List[SetoresResponse], name='solicitacoes')
def solicitacao(request: Request, db: Session = Depends(get_db)) -> List[SetoresResponse]:
    setores = db.query(Setores).all()
    context = {
        "request": request,
        "setores": setores
    }
    return TEMPLATES.TemplateResponse('solicitacoes.html', context=context)

# ----------------------      Rotas de Solicitações     --------------------

@router.get('/historico', name='historico')
def listar_solicitacao(request: Request, db: Session = Depends(get_db)):
    solicitacoes = db.query(Solicitacoes).all()
    for solicitacao in solicitacoes:
        setor = db.query(Setores).filter(Setores.id == solicitacao.id_setor).first()
        solicitacao.nome_setor = setor.nome if setor else "Setor não encontrado"

    context = {
        "request": request,
        "solicitacoes": solicitacoes
    }
    return TEMPLATES.TemplateResponse('historico.html', context=context)


@router.post('/criar-solicitacao', response_model=SolicitacoesResponse, status_code=201)
def criar_solicitacao(solicitacoes: SolicitacoesRequest, db: Session = Depends(get_db)) -> SolicitacoesResponse:
    # Verifica se o ID do setor fornecido existe na tabela setores
        setor = db.query(Setores).filter(Setores.id == solicitacoes.id_setor).first()
        if setor is None:
            raise HTTPException(status_code=404, detail="ID do setor não encontrado")
        
        nova_solicitacao = Solicitacoes(
            nome=solicitacoes.nome,
            matricula=solicitacoes.matricula,
            quantidade_resmas=solicitacoes.quantidade_resmas,
            id_setor=solicitacoes.id_setor
        )
        db.add(nova_solicitacao)
        db.commit()
        db.refresh(nova_solicitacao)

        return nova_solicitacao

        # return SolicitacoesResponse(
        #     **nova_solicitacao.__dict__
        # )


@router.put('/editar-solicitacao/{id_solicitacao}', status_code=204)
def editar_solicitacao(id_solicitacao: int, solicitacoes: SolicitacoesRequest, db: Session = Depends(get_db)) -> None:
    solicitacao:Solicitacoes = db.query(Solicitacoes).get(id_solicitacao)
    solicitacao.nome = solicitacoes.nome
    solicitacao.matricula = solicitacoes.matricula
    solicitacao.quantidade_resmas = solicitacoes.quantidade_resmas
    solicitacao.id_setor = solicitacoes.id_setor

    db.add(solicitacao)
    db.commit()
    db.refresh(solicitacao)
    return solicitacao

# @router.delete('/deletar-solicitacao/{id_solicitacao}', response_model=SolicitacoesResponse, status_code=200)
# def deletar_solicitacao(id_solicitacao: int, db: Session = Depends(get_db)) -> SolicitacoesResponse:

#     solicitacao = db.query(Solicitacoes).get(id_solicitacao)
#     db.delete(solicitacao)

#     db.commit()


@router.delete('/deletar-solicitacao/{id_solicitacao}', status_code=204)
def deletar_solicitacao(id_solicitacao: int, db: Session = Depends(get_db)):
    solicitacao = db.query(Solicitacoes).get(id_solicitacao)
    
    if solicitacao is None:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    
    db.delete(solicitacao)
    db.commit()


# ----------------------      Rotas de Impressões     --------------------
    

@router.get('/impressoes', response_model=List[SetoresResponse], name='impressoes')
def impressoes(request: Request, db: Session = Depends(get_db)) -> List[SetoresResponse]:
    setores = db.query(Setores).all()
    context = {
        "request": request,
        "setores": setores
    }
    return TEMPLATES.TemplateResponse('impressoes.html', context=context)


@router.get('/historico-impressoes', name='historico-impressoes')
def listar_impressoes(request: Request, db: Session = Depends(get_db)):
    impressoes = db.query(Impressoes).all()
    for impressao in impressoes:
        setor = db.query(Setores).filter(Setores.id == impressao.id_setor).first()
        impressao.nome_setor = setor.nome if setor else "Setor não encontrado"
        impressao.nome_impressora = setor.impressora if setor else "Impressora não encontrada"
    context = {
        "request": request,
        "impressoes": impressoes
    }
    return TEMPLATES.TemplateResponse('historico-impressoes.html', context=context)



@router.post('/criar-impressoes', response_model=ImpressoesResponse, status_code=201)
def criar_impressoes(impressoes: ImpressoesRequest, db: Session = Depends(get_db)) -> ImpressoesResponse:
    # Verifica se o ID do setor fornecido existe na tabela setores
    setor = db.query(Setores).filter(Setores.id == impressoes.id_setor).first()
    if setor is None:
        raise HTTPException(status_code=404, detail="ID do setor não encontrado")
    
    nova_impressao = Impressoes(
        quantidade_impressoes=impressoes.quantidade_impressoes,
        id_setor=impressoes.id_setor
    )
    db.add(nova_impressao)
    db.commit()
    db.refresh(nova_impressao)

    return nova_impressao


# ----------------------      Rotas de Relatório     --------------------

@router.get('/relatorio', response_model=List[SetoresResponse], name='relatorio')
def relatorio(request: Request, db: Session = Depends(get_db))-> List[SetoresResponse]:
    setores = db.query(Setores).all()
    context = {
        "request": request,
        "setores": setores
    }
    return TEMPLATES.TemplateResponse('relatorio.html', context=context)


@router.get('/relatorio-impressoes', response_model=List[SetoresResponse], name='relatorio-impressoes')
def relatorio(request: Request, db: Session = Depends(get_db))-> List[SetoresResponse]:
    setores = db.query(Setores).all()
    context = {
        "request": request,
        "setores": setores
    }
    return TEMPLATES.TemplateResponse('relatorio-impressoes.html', context=context)