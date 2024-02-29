from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession

from core.configs import URL_DATABASE, Base

engine: AsyncEngine = create_async_engine(URL_DATABASE, echo=False)

def get_session() -> AsyncSession:
    __async_session = sessionmaker(
        autocommit = False,
        autoflush= False,
        expire_on_commit= False,
        class_= AsyncSession,
        bind=engine
    )

    session: AsyncSession = __async_session()

    return session

async def create_tables() -> None:
    import models.__all_models
    print('Criando tabelas no banco de dados')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print('Tabelas criadas com sucesso')