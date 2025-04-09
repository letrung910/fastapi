fastapi dev main.py
fastapi run

uvicorn main:app --reload
uvicorn main:app --workers 4

### alembic
alembic revision -m "generate company table"
alembic revision -m "generate user table"
alembic revision -m "generate task table"
alembic upgrade <revesionid>

alembic downgrade base
alembic upgrade head


\l
\c fastapi
\dt
\d public.user

openssl rand -hex 32

