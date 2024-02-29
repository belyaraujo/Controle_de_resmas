from fastapi.routing import APIRouter
from fastapi.requests import Request

from core.configs import engine, SessionLocal, TEMPLATES, MEDIA

router = APIRouter()

@router.get('/', name='solicitacoes')
async def Solicitacoes(request: Request):
    context = {
        "request": request
    }
    
    return TEMPLATES.TemplateResponse('solicitacoes.html', context=context)

@router.get('/historico', name='historico')
async def Historico(request: Request):
    context = {
        "request": request
    }
    
    return TEMPLATES.TemplateResponse('historico.html', context=context)

@router.get('/relatorio', name='relatorio')
async def Relatorio(request: Request):
    context = {
        "request": request
    }
    
    return TEMPLATES.TemplateResponse('relatorio.html', context=context)