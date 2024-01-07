from pydantic import BaseModel, validator, ConfigDict, EmailStr
from typing import Optional
from pydantic.alias_generators import to_camel
from datetime import datetime


class EmailRegistrationSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    """Registration Email Schema"""
    user_id: Optional[str] = None
    email: EmailStr
    password: str
    kr_name: str
    sign_up_type: str = "email"
    register_at: Optional[datetime] = None


class RegistrationOauthSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    """Registration Email Schema"""
    user_id: Optional[str] = None
    kr_name: str
    sign_up_type: str
    email_verification: bool = True
    register_at: Optional[datetime] = None
