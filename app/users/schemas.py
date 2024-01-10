from typing import Optional, List
from pydantic import BaseModel


class UserResponseSchema(BaseModel):
    id: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    image_url: Optional[str]

    class Config:
        from_attributes = True


class EmailAddress(BaseModel):
    email_address: str = None
    id: str = None


class UserData(BaseModel):
    id: str = None
    first_name: str = None
    last_name: str = None
    image_url: str = None

    email_addresses: List[EmailAddress] = None
    phone_numbers: List[str] = None
    primary_email_address_id: str = None


class WebhookSchema(BaseModel):
    data: UserData = None
    type: str = None
