from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from router.auth import utils as auth_utils
from model.auth_model import LoginSchema
from model.db_model import UserAddressSchema
from model.registration_model import EmailRegistrationSchema


async def test_sign_in(form_data: LoginSchema, db: AsyncSession):
    user = await auth_utils.authenticate_user(
        db, LoginSchema(email=form_data.email, password=form_data.password)
    )
    if isinstance(user, int):
        raise Exception("404 또는 401 에러 발생")

    return {
        **user.model_dump(),
        **auth_utils.create_access_token_form(user.user_id).model_dump(by_alias=False),
    }


async def test_email_check(email: str, db: AsyncSession):
    user_info = await auth_utils.get_user_by_email(db, email)
    return {"isUnique": user_info is None}


async def test_register(
    user_registration: EmailRegistrationSchema, address: UserAddressSchema, db: AsyncSession
):
    user = await auth_utils.register_user_and_address(db, user_registration, address)

    if user is None:
        raise Exception("이미 존재하는 회원입니다.")

    return {**user.model_dump(), **auth_utils.create_access_token_form(user.user_id).model_dump()}


async def test_check_email_and_name(name: str, email: str, db: AsyncSession):
    user_info = await auth_utils.get_user_by_email_and_name(db, name, email)
    verification = user_info is not None
    if verification:
        return {
            "token": auth_utils.create_access_token_form(user_info.user_id).model_dump()[
                "access_token"
            ]
        }
    else:
        raise Exception("이메일과 아이디에 맞는 정보가 없습니다.")


async def test_update_password(db: AsyncSession, user_id: str, new_password: str):
    return await auth_utils.update_user_password(db=db, password=new_password, user_id=user_id)


def test_convert_token_to_user_id(token: str):
    token_data = auth_utils.get_current_user(token=token)
    return token_data.user_id
