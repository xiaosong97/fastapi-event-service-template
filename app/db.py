from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.settings import settings

# 数据库基础设施层（engine / Session / Base / 初始化）


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.DB_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    Base.metadata.create_all(bind=engine)
