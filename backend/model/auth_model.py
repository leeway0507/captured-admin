"""pydantic Schemas for Auth"""

from pydantic import BaseModel, EmailStr, ConfigDict
from model.db_model import UserSchema
from pydantic.alias_generators import to_camel
from typing import Optional


class LoginSchema(BaseModel):
    """user_login Schema"""

    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str


class LoginResponseSchema(Token):
    """login_response Schema"""

    # model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    user_id: str
    email: Optional[EmailStr] = None
    kr_name: str
    email_verification: bool
    sign_up_type: str
