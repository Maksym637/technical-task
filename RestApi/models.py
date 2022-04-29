from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, VARCHAR, DateTime

engine = create_engine('mysql+pymysql://root:Barca2381843@localhost/task')
engine.connect()

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
BaseModel = declarative_base()
BaseModel.query = Session.query_property()


class User(BaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(45))
    email = Column(VARCHAR(45))
    password = Column(VARCHAR(256))
    register_date = Column(DateTime)

    def __init__(self, username: str, email: str=None, password: str=None, register_date: datetime=None) -> None:
        self.username = username
        self.email = email
        self.password = password
        self.register_date = register_date
    
    def __str__(self) -> str:
        return f"id            : {self.id}\n" \
               f"username      : {self.username}\n" \
               f"email         : {self.email}\n" \
               f"password      : {self.password}\n" \
               f"register_date : {self.register_date}\n"


BaseModel.metadata.create_all(engine)