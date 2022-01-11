from sqlalchemy.orm import registry, Session
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+mysqlconnector://root:123456@localhost/account_book",
    echo=True,
    future=True
)
mapper_registry = registry()
Base = mapper_registry.generate_base()

mapper_registry.metadata.create_all(engine)
session = Session(engine)


class Account(Base):
    __tablename__ = "account"

    userid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(32), nullable=False)
    create_time = Column(
        TIMESTAMP,
        server_default=(text("CURRENT_TIMESTAMP"))
    )
    modification_time = Column(
        TIMESTAMP,
        server_default=(text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    )
