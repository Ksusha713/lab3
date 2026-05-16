from sqlmodel import Field, SQLModel

class Course(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    teacher: str
    credit: int
    semester: int

    