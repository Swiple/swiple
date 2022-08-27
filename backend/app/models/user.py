from app.models.base_model import BaseModel, validator
from pydantic import EmailStr


class User(BaseModel):
    display_name: str
    email: EmailStr
    password: str

    @validator("password")
    def valid_password(cls, v):
        if len(v) < 6:
            raise ValueError("length should be at least 6.")

        if len(v) > 60:
            raise ValueError("Length should be not be greater than 60.")

        if not any(char.isdigit() for char in v):
            raise ValueError("Password should have at least one numeral.")

        if not any(char.isupper() for char in v):
            raise ValueError("Password should have at least one uppercase letter.")

        if not any(char.islower() for char in v):
            raise ValueError("Password should have at least one lowercase letter.")

        return v
