from fastapi import FastAPI, Request, Form, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import fastapi.templating
from typing import Annotated
from data.db import create_course, get_all_courses, create_db_and_tables, get_session, create_user, get_user, check_password, get_all_users
from sqlmodel import Session

app = FastAPI()
favicon_path = 'static/images/favicon.ico'

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = fastapi.templating.Jinja2Templates(directory = "templates")

create_db_and_tables()

@app.get("/", response_class = HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request = request, name = "index.html"
    )

class SignUpForm(BaseModel):
    username: str   
    password: str
    repeat_password: str

class LoginForm(BaseModel):
    username: str   
    password: str

@app.get("/login", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html"
    )
    
@app.get("/signup", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, name="signup.html"
    )
    
@app.post("/signup")
async def signup(data: Annotated[SignUpForm, Form()], request: Request, session: Session = Depends(get_session)):
    if len(data.password) < 8:
        return templates.TemplateResponse(
            request=request, name="signup.html", context={"error": "Password is too short!"}
        )
    if data.password != data.repeat_password:
        return templates.TemplateResponse(
            request=request, name="signup.html", context={"error": "Passwords do not match!"}
        )
    already_user = get_user(session, data.username)
    if already_user:
        return templates.TemplateResponse(
            request=request, name="signup.html", context={"error": "Username is already taken!"}
        )
    user_role = "admin" if data.username.lower() == "admin" else "student"
    create_user(session, data.username, data.password, role=user_role)
    print(f"New user registered! {data.username}")
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/login")
async def login(data: Annotated[LoginForm, Form()], request: Request, session: Session = Depends(get_session)):
    user = get_user(session, data.username)
    if not user:
        return templates.TemplateResponse(
            request=request, name="login.html", context={"error": "The username doesn't exist. Try to sign up!"}
        )
    if not check_password(data.password, user.password):
        return templates.TemplateResponse(
            request=request, name="login.html", context={"error": "The username or password is not correct!"}
        )
    if user.role == "student":
        response = RedirectResponse(url="/user", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="user", value=user.name)
    else:
        response = RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="user", value=user.name)
    return response

@app.get("/user", response_class=HTMLResponse)
async def dashboard(request: Request):
    user_data = request.cookies.get("user")
    return templates.TemplateResponse(
        "userboard.html", {"request": request, "user_data": user_data}
    )
    
@app.get("/admin", response_class=HTMLResponse)
async def dashboard(request: Request, session: Session = Depends(get_session)):
    user_data = request.cookies.get("user")
    if not user_data:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    courses_list = get_all_courses(session)
    users_list = get_all_users(session)
    return templates.TemplateResponse(
        "admin.html", {"request": request, "user_data": user_data, "courses": courses_list, "users": users_list}
    )

@app.post("/admin/courses/add")
async def admin_add_course(title: Annotated[str, Form()], teacher: Annotated[str, Form()], credit: Annotated[int, Form()], semester: Annotated[int, Form()], session: Session = Depends(get_session)):
    create_course(session, title=title, teacher=teacher, credit=credit, semester=semester)
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
  
@app.get("/logout", response_class=HTMLResponse)
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER) 
    response.delete_cookie(key="user")
    return response