from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool 

class UserInDB(User):
    hashed_password: str


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )
