from typing import List
from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from users.utils import verify_webhook_signature
from db.database import get_db
from users.query import UsersQuery
from users.model import Users
from users.schemas import UserResponseSchema

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/webhook")
async def clerk_webhook(request: Request, session: Session = Depends(get_db)):
    webhook_payload = await verify_webhook_signature(request)

    users_query = UsersQuery(payload=webhook_payload, session=session)
    users_query.crud_user()

    try:
        session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return {"message": "Webhook received"}


@user_router.get("/")
async def get_users(session: Session = Depends(get_db)) -> List[UserResponseSchema]:
    users = session.query(Users).all()

    print(users)
    return users
