# Python API Lab

Python 3.14 / FastAPI. Без БД и внешних сервисов.

- Dockerfile, порт 8000; readiness: `GET /health`.
- Запуск: `python -m uvicorn app:app --host 0.0.0.0 --port 8000 --access-log`.
- Tests в контейнере: `python -m pytest -p no:cacheprovider tests`.
- UI: `GET /`. Корректный запрос: `POST /api/greet` с `{"name":"Ada"}` → 200.
- Неполный запрос: `POST /api/greet` с `{}` должен получать 400/422, а не 500.
- Runtime stdout/stderr и access-log uvicorn содержат диагностику.

## Запуск в Docker

```sh
docker build -t python-bug-lab .
docker run --rm -p 127.0.0.1:8001:8000 python-bug-lab
```

Откройте http://localhost:8001 и нажмите «Запрос без имени»: исходная версия
вернёт 500. Корректный запрос должен по-прежнему возвращать 200.

Регрессионные тесты: `docker run --rm python-bug-lab python -m pytest -p no:cacheprovider tests`.
В исходной версии тест валидации намеренно падает: цель задания — исправить приложение.

## Проверка агентом

URL: https://github.com/SergeiM89/python-bug-lab. Ветка по умолчанию `main`
содержит API-дефект; `demo/api` — тот же исходный сценарий. Ветка `demo/build`
содержит отдельный дефект сборки. `baseline/healthy` — исправный контрольный вариант.
Для повторения используйте новый сеанс с выбранной веткой.

Исправления сначала выполняются и проверяются локально. Публикация PR — отдельное
действие после проверки результата и подключения GitHub с правом записи.
