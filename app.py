import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="Python bug laboratory")
logger = logging.getLogger("uvicorn.error")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def page():
    return """<!doctype html><html lang="ru"><meta charset="utf-8"><title>Python API Lab</title>
    <style>body{font:18px system-ui;max-width:700px;margin:60px auto;background:#101822;color:#eef}
    button{padding:16px;margin:8px;border-radius:8px;background:#64d4b0;cursor:pointer}pre{white-space:pre-wrap}</style>
    <h1>Python API Lab</h1><p>Проверка API с корректным и неполным JSON.</p>
    <button onclick='send({name:"Ada"})'>Корректный запрос</button>
    <button onclick='send({})'>Запрос без имени</button><pre id="result"></pre>
    <script>async function send(body){let r=await fetch('/api/greet',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    document.getElementById('result').textContent=r.status+' '+await r.text()}</script></html>"""


@app.post("/api/greet")
async def greet(request: Request):
    data = await request.json()
    if not isinstance(data, dict) or not isinstance(data.get('name'), str) or not data['name'].strip():
        raise HTTPException(status_code=422, detail='name is required')
    return {"message": f"Hello, {data['name']}!"}
