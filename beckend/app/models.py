from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base



class User(Base):
    __tablename__ = "users"    

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    disabled = Column(Boolean)
    hashed_password = Column(String)


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )
