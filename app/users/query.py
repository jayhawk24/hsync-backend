from pydantic import EmailStr
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from users.model import Users
from users.schemas import WebhookSchema


class UsersQuery:
    def __init__(self, payload: WebhookSchema, session: Session) -> None:
        self.payload = payload
        self.session = session
        self.payload_data = payload.data

    def validate_payload(self):
        if self.payload.type not in [
            "user.created",
            "user.deleted",
            "user.updated",
        ]:
            return {
                "message": "Webhook received",
                "type": self.payload.type,
                "action": "No action needed.",
            }

    @staticmethod
    def _get_clerk_email(payload: WebhookSchema) -> EmailStr:
        primary_email_id = payload.data.primary_email_address_id
        email = next(
            filter(
                lambda x: x.get("id") == primary_email_id, payload.data.email_addresses
            ),
            None,
        )
        if email == None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No email provided"
            )
        return email["email_address"]

    def create_user(self):
        data = self.payload.data
        email = self._get_clerk_email(self.payload)
        user = Users(
            id=self.payload.data.id,
            email=email,
            first_name=data.first_name,
            last_name=data.last_name,
            image_url=data.image_url,
        )
        self.session.add(user)

        return user

    def update_user(self):
        payload_data = self.payload.data
        user = self.session.query(Users).filter_by(id=self.payload_data.id).first()
        user.first_name = payload_data.first_name
        user.last_name = payload_data.last_name
        user.email = self._get_clerk_email(self.payload)
        user.image_url = payload_data.image_url

        self.session.flush()

    def delete_user(self):
        self.session.query(Users).filter_by(id=self.payload_data.id).delete()

    def crud_user(self):
        is_valid = self.validate_payload()
        if isinstance(is_valid, dict):
            return is_valid

        if self.payload.type == "user.created":
            return self.create_user()
        if self.payload.type == "user.updated":
            return self.update_user()
        if self.payload.type == "user.deleted":
            return self.delete_user()
