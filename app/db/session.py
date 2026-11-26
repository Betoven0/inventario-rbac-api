from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

#1 Compatibilidad multi-motor (SQLite en local vs PostgreSQL en produccion)
connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

#2 Motor de conexiones asincrono 
engine = create_async_engine(
    settings.DATABASE_URL,
    echo= False,
    connect_args= connect_args
)

#3 Fabrica de sessiones (una sesion por cada peticion HTTP)
AsyncSessionLocal = async_sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit = False,
    autocommit = False, 
    autoflush = False
)

#4 Inyector de dependencias para FastAPI

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Abre una session de BD al inicias la peticion y la cierra al terminar"""
    async with AsyncSessionLocal() as session:
        yield session