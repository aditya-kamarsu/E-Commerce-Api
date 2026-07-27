from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase




engine = create_engine(
    "sqlite:///create_db",
    echo=True
)



SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)




class Base(DeclarativeBase):
    pass