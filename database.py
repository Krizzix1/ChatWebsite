from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database/testBase.db", echo=False)

Base = declarative_base()

class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, autoincrement=True)
    words = Column(String)

    def __repr__(self):
        return f"(ID = {self.id}, words = '{self.words}')"

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def add_entry(text):
    with Session() as session:
        entry = Test(words = text)
        session.add(entry)
        session.commit()

def query_all():
    with Session() as session:
        rows = session.query(Test).all()
        for row in rows:
            print(row)

