from sqlmodel import Session, SQLModel, create_engine, select
from models.courses import Course
from models.users import User
import bcrypt

sqlite_file_name = "app.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_course(session: Session, title: str, teacher: str, credit: int, semester: int):
    new_course = Course(title=title, teacher=teacher, credits=credit, semester=semester)
    session.add(new_course)
    session.commit()
    session.refresh(new_course)
    return new_course

def get_all_courses(session: Session):
    statement = select(Course)
    results = session.exec(statement)
    return results.all()

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    return hashed_password

def create_user(session: Session, name: str, password: str, role: str="student"):
    hashed_password = hash_password(password)
    new_user = User(name=name, password=hashed_password, role=role)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def get_user(session: Session, username: str):
    statement = select(User).where(User.name == username)
    results = session.exec(statement).first()
    return results

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))