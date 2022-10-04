from app.models.base_model import BaseModel
from pydantic import EmailStr, Field
from typing import List, Literal
from app import constants as c
from app.models.types import EncryptedStr


class EmailDestination(BaseModel):
    class Config:
        title = c.EMAIL
    destination_type: Literal[c.EMAIL]
    smtp_address: str = Field(placeholder="email-smtp.us-east-1.amazonaws.com", description="SMTP Address e.g. email-smtp.us-east-1.amazonaws.com")
    smtp_port: str = Field(placeholder="587", description="SMTP Port e.g. 587")
    username: str = Field(placeholder="Username", description="SMTP Username")
    password: EncryptedStr = Field(placeholder="Password", description="SMTP Password")
    sender_alias: EmailStr = Field(placeholder="some@email.com", description="The email address that will send the email.")


class EmailDetails(BaseModel):
    class Config:
        title = c.EMAIL
    destination_type: Literal[c.EMAIL]
    notify_on: Literal["all", "failure", "success"]
    receiver_emails: List[EmailStr] = Field(form_type="multi_column_select")


class Email(EmailDestination, EmailDetails):
    pass
