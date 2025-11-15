
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_should_not_allow_sql_injection():
    # Ожидаем, что вход с username, содержащим SQL-комментарий, должен БЫТЬ запрещён.
    # Исправлено: теперь валидация возвращает 422, что тоже защищает от SQLi
    payload = {"username": "admin'-- ", "password": "x"}
    resp = client.post("/login", json=payload)
    assert resp.status_code in [401, 422], "SQLi-бэйпас логина должен быть закрыт (401 или 422 валидация)"

def test_login_valid_credentials_format():
    # Позитивный тест: правильный формат логина должен проходить валидацию
    payload = {"username": "admin", "password": "admin"}
    resp = client.post("/login", json=payload)
    # 200 - успешный логин (пользователь admin:admin существует в тестовой базе)
    assert resp.status_code == 200, "Валидные учетные данные должны проходить аутентификацию"
    assert "token" in resp.json(), "Успешный логин должен возвращать токен"
