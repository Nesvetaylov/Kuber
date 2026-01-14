import os
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "SuperSecretPassword123")
DB_HOST = "postgres-service"
DB_NAME = "user_management"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    status = Column(String, default="active")

Base.metadata.create_all(bind=engine)
app = FastAPI()

# СТРАНИЦЫ ИНТЕРФЕЙСА

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>Главная</title></head>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
            <h1>Добро пожаловать в UserApp</h1>
            <p>Это главная страница приложения.</p>
            <a href="/login-page"><button style="padding: 10px 20px;">Войти в систему</button></a>
            <a href="/register-page"><button style="padding: 10px 20px;">Регистрация</button></a>
        </body>
    </html>
    """

@app.get("/register-page", response_class=HTMLResponse)
def register_page():
    return """
    <html>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
            <h2>Регистрация нового пользователя</h2>
            <form action="/register" method="post">
                <input type="text" name="username" placeholder="Логин" required>

                <input type="password" name="password" placeholder="Пароль" required>

                <button type="submit">Создать аккаунт</button>
            </form>
        </body>
    </html>
    """

@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    return """
    <html>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
            <h2>Вход в систему</h2>
            <form action="/login-ui" method="post">
                <input type="text" name="username" placeholder="Логин" required>

                <input type="password" name="password" placeholder="Пароль" required>

                <button type="submit">Войти</button>
            </form>
        </body>
    </html>
    """

# ЛОГИКА ОБРАБОТКИ ФОРМ

@app.post("/register") 
def register(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    try:
        new_user = User(username=username, password=password)
        db.add(new_user)
        db.commit()
        return HTMLResponse("<h2>Регистрация успешна!</h2><a href='/login-page'>Перейти к входу</a>")
    except Exception as e:
        return f"Ошибка: {e}"
    finally:
        db.close()

@app.post("/login-ui")
def login_ui(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username, User.password == password).first()
    db.close()
    if user:
        return HTMLResponse(f"""
            <body style="font-family: Arial; padding: 20px;">
                <h1>Личная страница пользователя</h1>
                <hr>
                <p><b>ID:</b> {user.id}</p>
                <p><b>Логин:</b> {user.username}</p>
                <p><b>Статус:</b> <span style="color: green;">{user.status}</span></p>
                

                <a href="/">Выйти</a>
            </body>
        """)
    raise HTTPException(status_code=401, detail="Неверные данные")

"/register"
def register(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    try:
        new_user = User(username=username, password=password)
        db.add(new_user)
        db.commit()
        return HTMLResponse("<h2>Регистрация успешна!</h2><a href='/login-page'>Перейти к входу</a>")
    except:
        return "Ошибка: пользователь уже существует."
    finally:
        db.close()

"/login-ui"
def login_ui(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username, User.password == password).first()
    db.close()
    if user:
        return HTMLResponse(f"""
            <body style="font-family: Arial; padding: 20px;">
                <h1>Личная страница пользователя</h1>
                <hr>
                <p><b>ID:</b> {user.id}</p>
                <p><b>Логин:</b> {user.username}</p>
                <p><b>Статус:</b> <span style="color: green;">{user.status}</span></p>
                

                <a href="/">Выйти</a>
            </body>
        """)
    raise HTTPException(status_code=401, detail="Неверные данные")

@app.get("/health/live")
def health_live():
    return {"status": "alive"}

@app.get("/health/ready")
def health_ready():
    return {"status": "ready"}