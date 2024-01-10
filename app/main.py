from fastapi import FastAPI, HTTPException
from db.database import check_db_connection
from users.handler import user_router

app = FastAPI()
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/ping")
async def ping_pong():
    return {"ping": "pong!"}


# Heartbeat endpoint
@app.get("/heartbeat", tags=["heartbeat"])
async def heartbeat():
    if check_db_connection():
        return {"message": "Database connection is healthy."}
    else:
        raise HTTPException(status_code=500, detail="Database connection error")
