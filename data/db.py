from sqlmodel import Session, SQLModel, create_engine, select
from passlib.context import CryptContext

from models.courses import Course
from models.users import User

sqlite_file_name = "app.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_course(title: str, teacher: str, credit: int, semester: int):
    with Session(engine) as session:
        new_course = Course(title=title, teacher=teacher, credits=credit, semester=semester)
        session.add(new_course)
        session.commit()
        session.refresh(new_course)
        return new_course

def get_all_courses():
    with Session(engine) as session:
        statement = select(Course)
        results = session.exec(statement)
        return results.all()

def create_user(name: str, password: str):
    with Session(engine) as session:
        hashed_password = pwd_context.hash(password)
        new_user = User(name=name, password=hashed_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

def get_user(username: str):
    with Session(engine) as session:
        statement = select(User).where(User.name == username)
        results = session.exec(statement).first()
        return results