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
    email_address: Optional[str]
    id: Optional[str]
    linked_to: Optional[List[str]]


class UserData(UserResponseSchema):
    id: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    image_url: Optional[str]

    email_addresses: Optional[List[EmailAddress]]
    phone_numbers: Optional[List[str]]
    primary_email_address_id: Optional[str]


class WebhookSchema(BaseModel):
    data: Optional[UserData]
    type: Optional[str]
