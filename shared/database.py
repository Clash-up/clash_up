import asyncio
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DatabaseManager:
    """
    Centralny menedżer połączeń do zewnętrznych baz danych (różnych dialektów) oparty na
    SQLAlchemy 2.0 i trybie asynchronicznym. Jego głównym celem jest ponowne wykorzystywanie
    (pesymistyczne cache'owanie) silników `AsyncEngine` - co pozwala ograniczyć koszty tworzenia
    pooli połączeń podczas wielokrotnych migracji wykonywanych równolegle.

    Przykładowe użycie::

        from module import DatabaseManager
        SessionMaker = DatabaseManager.get_async_sessionmaker(source_url)
        async with SessionMaker() as session:
            ...  # używaj sesji tak samo jak w głównej bazie

        # sprawdź, czy baza żyje
        is_alive = await DatabaseManager.ping(source_url)
    """

    _engines: dict[str, AsyncEngine] = {}
    _sessionmakers: dict[str, async_sessionmaker[AsyncSession]] = {}
    _locks: defaultdict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

    @staticmethod
    def _key(url: str) -> str:
        u = make_url(url)
        # kanonizacja: bez hasła w kluczu (żeby zmiana hasła wymuszała świadome odświeżenie)
        return u._replace(password=None).render_as_string(hide_password=True)

    @classmethod
    async def get_engine(cls, url: str, *, echo: bool = False, **engine_kwargs) -> AsyncEngine:
        """
        Pobiera lub tworzy silnik `AsyncEngine` dla podanego URL bazy danych.

        Args:
            url (str): URL bazy danych.
            echo (bool): Czy logować zapytania SQL.
            **engine_kwargs: Dodatkowe argumenty przekazywane do `create_async_engine`.

        Returns:
            AsyncEngine: Silnik bazy danych.
        """
        engine_kwargs.setdefault("pool_pre_ping", True)
        engine_kwargs.setdefault("pool_recycle", 180)  # 3 minuty
        key = cls._key(url)
        if key in cls._engines:
            return cls._engines[key]
        lock = cls._locks[key]
        async with lock:
            if key in cls._engines:
                return cls._engines[key]
            engine = create_async_engine(url, echo=echo, **engine_kwargs)
            cls._engines[key] = engine
            return engine

    @classmethod
    async def get_async_sessionmaker(
        cls,
        url: str,
        *,
        expire_on_commit: bool = False,
        echo: bool = False,
    ) -> async_sessionmaker:
        """
        Pobiera lub tworzy `async_sessionmaker` dla podanego URL bazy danych.

        Args:
            url (str): URL bazy danych.
            expire_on_commit (bool): Czy wygaszać obiekty po commit.
            echo (bool): Czy logować zapytania SQL.

        Returns:
            async_sessionmaker: Fabryka sesji bazy danych.
        """
        url = cls._key(url)
        if url in cls._sessionmakers:
            return cls._sessionmakers[url]
        lock = cls._locks[url]
        async with lock:
            if url in cls._sessionmakers:
                return cls._sessionmakers[url]
            engine = await cls.get_engine(url, echo=echo)
            cls._sessionmakers[url] = async_sessionmaker(
                bind=engine, expire_on_commit=expire_on_commit
            )
            return cls._sessionmakers[url]

    @classmethod
    @asynccontextmanager
    async def session(
        cls,
        url: str,
        *,
        expire_on_commit: bool = False,
        echo: bool = False,
    ) -> AsyncGenerator[AsyncSession, None]:
        """
        Asynchroniczny kontekst menedżera sesji bazy danych.

        Args:
            url (str): URL bazy danych.
            expire_on_commit (bool): Czy wygaszać obiekty po commit.
            echo (bool): Czy logować zapytania SQL.

        Yields:
            AsyncSession: Sesja bazy danych.

        Usage:
            async with DatabaseManager.session(url) as session:
                # używaj sesji tak samo jak w głównej bazie
        """
        SessionLocal = await cls.get_async_sessionmaker(
            url, expire_on_commit=expire_on_commit, echo=echo
        )
        async with SessionLocal() as session:
            yield session

    @classmethod
    async def dispose_engine(cls, url: str) -> None:
        """
        Zamyka i usuwa silnik `AsyncEngine` dla podanego URL bazy danych.
        Args:
            url (str): URL bazy danych.
        """
        engine = cls._engines.pop(cls._key(url), None)
        if engine:
            await engine.dispose()
        cls._sessionmakers.pop(cls._key(url), None)
        cls._locks.pop(cls._key(url), None)

    @classmethod
    async def dispose_all_engines(cls) -> None:
        """
        Zamyka i usuwa wszystkie silniki `AsyncEngine`.
        """
        for engine in cls._engines.values():
            await engine.dispose()
        cls._engines.clear()
        cls._sessionmakers.clear()
        cls._locks.clear()

    @classmethod
    async def ping(cls, url: str) -> bool:
        """
        Sprawdza, czy połączenie z bazą danych jest aktywne.

        Args:
            url (str): URL bazy danych.

        Returns:
            bool: True, jeśli połączenie jest aktywne, False w przeciwnym razie.
        """
        engine = await cls.get_engine(url)
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False


async def init_models(async_engine: AsyncEngine) -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
