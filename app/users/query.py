from pydantic import EmailStr
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from users.model import Users


class UsersQuery:
    def __init__(self, payload, session: Session) -> None:
        self.payload = payload
        self.session = session

    def validate_payload(self):
        if self.payload.get("type") not in [
            "user.created",
            "user.deleted",
            "user.updated",
        ]:
            return {
                "message": "Webhook received",
                "type": self.payload.get("type"),
                "action": "No action needed.",
            }

    @staticmethod
    def _get_clerk_email(payload) -> EmailStr:
        primary_email_id = payload.get("data").get("primary_email_address_id")
        email = next(
            filter(
                lambda x: x.get("id") == primary_email_id,
                payload.get("data").get("email_addresses"),
            ),
            None,
        )
        if email == None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No email provided"
            )
        return email["email_address"]

    def create_user(self):
        data = self.payload.get("data")
        email = self._get_clerk_email(self.payload)
        user = Users(
            id=self.payload.get("data").get("id"),
            email=email,
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            image_url=data.get("image_url"),
        )
        self.session.add(user)

        return user

    def update_user(self):
        pass

    def delete_user(self):
        pass

    def crud_user(self):
        is_valid = self.validate_payload()
        if isinstance(is_valid, dict):
            return is_valid

        if self.payload.get("type") == "user.created":
            return self.create_user()
