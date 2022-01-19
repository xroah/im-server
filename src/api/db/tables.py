from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from .main import Base


class Account(Base):
    __tablename__ = "account"

    userid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(32), nullable=False)
    email = Column(String(40))
    mobile = Column(String(11))
    create_time = Column(
        TIMESTAMP,
        server_default=(text("CURRENT_TIMESTAMP"))
    )
    modification_time = Column(
        TIMESTAMP,
        server_default=(text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    )
