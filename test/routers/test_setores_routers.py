from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from configs.database import Base
from configs.dependencies import get_db

from main import app

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    response = client.post('/criar-solicitacao', json={
        "nome": "raimundo",
        "matricula": "1234",
        "quantidade_resmas": 1,
        "id_setor": 1
    })
    response = client.post('/criar-solicitacao', json={
        "nome": "string",
        "matricula": "4321",
        "quantidade_resmas": 5,
        "id_setor": 1
    })

    response = client.get('/')

    assert response.status_code == 200
    # assert response.json() == [{
    #     "nome": "string",
    #     "matricula": "4321",
    #     "quantidade_resmas": 5,
    #     "id_setor": 1
    # }]


def test_criar_solicitacao():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    novo_setor = {
        "nome": "string",
        "matricula": "string",
        "quantidade_resmas": "1",
        "id_setor": 1
    }

    novo_setor_copy = novo_setor.copy()

    novo_setor_copy["id"] = 1

    response = client.post('/criar-solicitacao', json=novo_setor)
    assert response.status_code == 201
    assert response.json() == novo_setor_copy
    

def test_atualizar_solicitacao():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)


    response = client.post('/criar-solicitacao', json={
        "nome": "string",
        "matricula": "string",
        "quantidade_resmas": "1",
        "id_setor": 1
    })

    id_solicitacao = response.json()['id']


    response_put = client.put(f'/editar-solicitacao/{id_solicitacao}', json={
            "nome": "string",
            "matricula": "1111",
            "quantidade_resmas": "1",
            "id_setor": 1
        })

    assert response_put.status_code == 200
    assert response_put.json()['matricula'] == 1111


def test_deletar_solicitacao():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)


    response = client.post('/criar-solicitacao', json={
        "nome": "string",
        "matricula": "string",
        "quantidade_resmas": "1",
        "id_setor": 1
    })

    id_solicitacao = response.json()['id']


    response_put = client.delete(f'/deletar-solicitacao/{id_solicitacao}')

    assert response_put.status_code == 204
