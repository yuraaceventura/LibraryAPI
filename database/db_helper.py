from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session

from config.config import settings


class DatabaseHelper:
    def __init__(self):
        self.engine = create_async_engine(settings.database.get_url())
        self.session_factory = async_sessionmaker(bind=self.engine,expire_on_commit=False, autocommit=False, autoflush=False)

    def get_scoped_session(self):
        return async_scoped_session(self.session_factory, scopefunc=current_task)

    async def get_session(self):
        try:
            session = self.get_scoped_session()
            yield session
        finally:
            await session.close()

db_helper = DatabaseHelper()
