from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import fastapi.templating
from typing import Annotated
from data.usersdb import users

app = FastAPI()
favicon_path = 'static/images/favicon.ico'

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = fastapi.templating.Jinja2Templates(directory = "templates")

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
async def signup(data: Annotated[SignUpForm, Form()], request: Request):
    if data.username in users:
        return templates.TemplateResponse(
            request=request, name="signup.html", context={"error": "Username is already taken!"}
        )
    if len(data.password) < 8:
        return templates.TemplateResponse(
            request=request, name="signup.html", context={"error": "Password is too short!"}
        )
    if data.password != data.repeat_password:
        return templates.TemplateResponse(
            request=request, name="signup.html", context={"error": "Passwords do not match!"}
        )
    users[data.username] = {
        "password": data.password,
        "role": "student"
    }
    print(f"New user registered! Current DB: {users}")
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/login")
async def login(data: Annotated[LoginForm, Form()], request: Request):
    profile = users[data.username]
    if profile["password"] != data.password:
        return templates.TemplateResponse(
            request=request, name="login.html", context={"error": "The username or password is not correct!"}
        )
    if data.username not in users:
        return templates.TemplateResponse(
            request=request, name="login.html", context={"error": "The username doesn't exist. Try to sign up!"}
        )
    if profile["role"] == "student":
        response = RedirectResponse(url="/user", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="user", value=data.username)
    if profile["role"] == "admin":
        response = RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="user", value=data.username)
    return response

@app.get("/user", response_class=HTMLResponse)
async def dashboard(request: Request):
    user_data = request.cookies.get("user")
    return templates.TemplateResponse(
        "userboard.html", {"request": request, "user_data": user_data}
    )
@app.get("/admin", response_class=HTMLResponse)
async def dashboard(request: Request):
    user_data = request.cookies.get("user")
    return templates.TemplateResponse(
        "admin.html", {"request": request, "user_data": user_data}
    )
    
@app.get("/logout", response_class=HTMLResponse)
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER) 
    response.delete_cookie(key="user")
    return response