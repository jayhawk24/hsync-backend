from fastapi import FastAPI, HTTPException
from db.database import check_db_connection

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Heartbeat endpoint
@app.get("/heartbeat", tags=["heartbeat"])
async def heartbeat():
    if check_db_connection():
        return {"message": "Database connection is healthy."}
    else:
        raise HTTPException(status_code=500, detail="Database connection error")
