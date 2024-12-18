from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import security


engine = create_engine("sqlite:///database/testBase.db", echo=False)

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String, unique=True)
    password = Column(String)
    salt = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def add_user(username, password):
    with Session() as session:
        pass_salt = security.gen_salt()
        user = Users(userName = username, password = security.hash_pass(password, pass_salt), salt = pass_salt)
        session.add(user)
        session.commit()


def get_user_salt(username):
    with Session() as session:
        user = session.query(Users).filter(Users.userName == username).first()
        if user:
            return user.salt
        else:
            return None
        

def validate_user_password(username, password):
    with Session() as session:
        user = session.query(Users).filter(Users.userName == username).first()

        if user:
            if user.password == security.hash_pass(password, get_user_salt(username)):
                return True
            else:
                return False
        else:
            return None


def query_all():
    with Session() as session:
        rows = session.query(Users).all()
        for row in rows:
            print(row)


def existing_user(username):
    with Session() as session:
        users = session.query(Users).all()
        for user in users:
            if user.userName == username:
                print(f"user.userName {user.userName} == username {username}")
                return True
        return False
