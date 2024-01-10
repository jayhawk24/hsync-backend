from typing import Optional
from pydantic import BaseModel


class UserResponseSchema(BaseModel):
    id: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    image_url: Optional[str]

    class Config:
        from_attributes = True
