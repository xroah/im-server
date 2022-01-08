from sqlalchemy import create_engine

engine = create_engine(
    "mysql+mysqlconnector://root:123456@localhost/account_book",
    echo=True,
    future=True
)
