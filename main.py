import uvicorn

import databases
from database import database
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

from users.routes import router as user_router

app = FastAPI(debug=True)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(user_router, prefix='/users')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
