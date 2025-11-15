
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED

from .models import LoginRequest
from .db import query, query_one, query_one_params, query_params

app = FastAPI(title="secdev-seed-s06-s08")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request, msg: Optional[str] = None):
    # XSS: намеренно рендерим message без экранирования через шаблон (см. index.html)
    return templates.TemplateResponse("index.html", {"request": request, "message": msg or "Hello!"})

@app.get("/echo", response_class=HTMLResponse)
def echo(request: Request, msg: Optional[str] = None):
    return templates.TemplateResponse("index.html", {"request": request, "message": msg or ""})

@app.get("/search")
def search(q: Optional[str] = Query(default=None, min_length=1, max_length=32)):
    # Исправлено: используем параметризованный запрос
    if q:
        pattern = f"%{q}%"
        sql = "SELECT id, name, description FROM items WHERE name LIKE ?"
        items = query_params(sql, (pattern,))
    else:
        sql = "SELECT id, name, description FROM items LIMIT 10"
        items = query(sql)
    return JSONResponse(content={"items": items})

@app.post("/login")
def login(payload: LoginRequest):
    # Исправлено: используем параметризованный запрос
    sql = "SELECT id, username FROM users WHERE username = ? AND password = ?"
    row = query_one_params(sql, (payload.username, payload.password))
    if not row:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # фиктивный токен
    return {"status": "ok", "user": row["username"], "token": "dummy"}
