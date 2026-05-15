from sqlmodel import Session, SQLModel, create_engine, select
from data.coursesdb import Course

sqlite_file_name = "courses.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

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