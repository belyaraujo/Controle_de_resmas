from fastapi import FastAPI


from routers import home_view
from configs.database import Base, engine

from models.setores_model import Setores
from models.solicitacoes_model import Solicitacoes
from models.impressoes_model import Impressoes

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

app = FastAPI()


# @app.get('/')
# def home():
#     return "oi"

app.include_router(home_view.router)