from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse

# Local teaching fixture: Starlette returns real unhandled tracebacks in HTTP 500 responses.
app = FastAPI(title="Python bug laboratory", debug=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def page():
    return """<!doctype html><html lang="ru"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1"><title>Python API Lab</title>
    <style>
    *{box-sizing:border-box}body{font:17px/1.6 system-ui;margin:0;background:#101822;color:#eef2ff}
    main{max-width:860px;margin:48px auto;padding:0 24px}h1{margin-bottom:8px}
    p{color:#b8c6d9}.buttons{display:flex;flex-wrap:wrap;gap:12px;margin:24px 0}
    button{font:inherit;padding:12px 18px;border:1px solid #64d4b0;border-radius:10px;
    background:#64d4b0;color:#10231d;cursor:pointer}button+button{background:transparent;color:#eef2ff}
    button:disabled{opacity:.55;cursor:wait}section{padding:20px;border:1px solid #34445a;border-radius:12px}
    section[data-kind="error"]{border-color:#ff7e88}section[data-kind="handled"]{border-color:#e7bf72}
    section[data-kind="success"]{border-color:#64d4b0}h2{font-size:20px;margin:0}
    pre{white-space:pre-wrap;overflow-wrap:anywhere;max-height:55vh;overflow:auto;
    background:#0a1019;padding:16px;border-radius:8px;font:14px/1.5 ui-monospace,monospace}
    [hidden]{display:none}
    </style></head><body><main><h1>Python API Lab</h1>
    <p>Отправьте запрос: ниже появятся HTTP-статус, сообщение и диагностика backend.</p>
    <div class="buttons"><button onclick='send({name:"Ada"})'>Корректный запрос</button>
    <button onclick='send({})'>Запрос без имени</button></div>
    <section id="response" hidden aria-busy="false"><h2 id="result-status" role="status" aria-live="polite"></h2>
    <p id="result-message"></p><pre id="result" tabindex="0" aria-label="Ответ и traceback backend"></pre></section>
    <script>
    async function send(body){
      const panel=document.getElementById('response'),status=document.getElementById('result-status');
      const message=document.getElementById('result-message'),result=document.getElementById('result');
      const buttons=document.querySelectorAll('button');
      panel.hidden=false;panel.dataset.kind='';panel.setAttribute('aria-busy','true');
      status.textContent='Отправляем запрос…';message.textContent='';result.textContent='';
      buttons.forEach(button=>button.disabled=true);
      try{
        const response=await fetch('/api/greet',{method:'POST',
          headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(body)});
        const text=await response.text();let data=null;
        try{data=JSON.parse(text)}catch{}
        result.textContent=data===null?text:JSON.stringify(data,null,2);
        result.scrollTop=0;
        if(response.status>=500){
          panel.dataset.kind='error';status.textContent='HTTP '+response.status+' · Ошибка backend';
          message.textContent=data?.exception||text.trim().split('\\n').pop()||'Необработанная ошибка сервера';
        }else if(!response.ok){
          panel.dataset.kind='handled';status.textContent='HTTP '+response.status+' · Запрос отклонён';
          message.textContent=typeof data?.detail==='string'?data.detail:'Backend обработал некорректный запрос.';
        }else{
          panel.dataset.kind='success';status.textContent='HTTP '+response.status+' · Успешно';
          message.textContent=data?.message||'Запрос выполнен.';
        }
      }catch(error){
        panel.dataset.kind='error';status.textContent='Нет соединения с backend';message.textContent=error.message;
      }finally{panel.setAttribute('aria-busy','false');buttons.forEach(button=>button.disabled=false)}
    }
    </script></main></body></html>"""


@app.post("/api/greet")
async def greet(request: Request):
    data = await request.json()
    if not isinstance(data, dict) or not isinstance(data.get('name'), str) or not data['name'].strip():
        raise HTTPException(status_code=422, detail='Запрос отклонён: поле name обязательно и должно быть непустой строкой.')
    return {"message": f"Hello, {data['name']}!"}
