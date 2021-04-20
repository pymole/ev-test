from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import settings


engine = create_engine(
    'postgresql://{}:{}@{}:{}/{}'.format(
        settings.global_settings.db_user,
        settings.global_settings.db_password,
        settings.global_settings.db_host,
        settings.global_settings.db_port,
        settings.global_settings.db_name,
    )
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


context_session = contextmanager(get_session)
