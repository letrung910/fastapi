from typing import Union
from fastapi import FastAPI
from routers import company, auth, user, task
app = FastAPI()
app.include_router(company.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(task.router)

@app.get("/")
async def health_check():
    return "Api is running"

