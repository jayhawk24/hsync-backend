from db.database import Base
from sqlalchemy import Column, VARCHAR, String


class Users(Base):
    __tablename__ = "users"

    id = Column(VARCHAR(100), primary_key=True, index=True)
    first_name = Column(VARCHAR(50), nullable=False)
    last_name = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(100), unique=True, nullable=False)

    image_url = Column(String(512))
