from sqlalchemy.orm import registry, Session
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