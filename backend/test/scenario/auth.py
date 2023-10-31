from sqlalchemy import delete

from test_module.auth import *
from variables import get_register_info, get_address_info
from db.tables import UserTable, UserAddressTable


async def auth_scenario(db):
    register_info = get_register_info()
    address_info = get_address_info()
    form_data = LoginSchema(email=register_info.email, password=register_info.password)
    new_password = "test1234"

    # 중복 이메일 체크 => Unique
    # 회원가입
    # 중복 이메일 체크 => duplicated
    # 로그인
    # 이메일, 아이디 체크
    # token => user_id
    # 비밀번호 변경
    # 주소 제거
    # 아이디 제거

    # user_id = "8da1746472ea11eebdcf56c54ce9fb27"
    # await delete_address_force(db=db, user_id=user_id)
    # await delete_user(db=db, user_id=user_id)

    print("----------auth_scenario 시작----------")
    await check_email_before_registration(db=db, email=register_info.email)
    await register_user_and_address(db=db, register_info=register_info, address_info=address_info)
    await check_email_after_registration(db=db, email=register_info.email)

    user_info = await login(db=db, form_data=form_data)
    token = await check_email_and_name(db=db, name=register_info.kr_name, email=register_info.email)

    assert token != None, "token이 존재해야합니다."
    user_id = convert_token_to_user_id(token=token)
    assert user_id == user_info.get("user_id"), f"{user_id} != {user_info.get('user_id')}"

    await update_password(
        db=db, new_password=new_password, user_id=user_id, email=register_info.email
    )
    await delete_address_force(db=db, user_id=user_id)
    await delete_user(db=db, user_id=user_id)

    print("----------auth_scenario 종료----------")


# Part --------------------------------------------------------------


async def check_email_before_registration(db: AsyncSession, email: str):
    result = await test_email_check(db=db, email=email)
    print("---check_email_before_registration---")
    print(result)
    assert result.get("isUnique") == True, "True로 return 해야합니다."


async def register_user_and_address(
    db: AsyncSession, register_info: EmailRegistrationSchema, address_info: UserAddressSchema
):
    result = await test_register(db=db, user_registration=register_info, address=address_info)
    print("---register_user_and_address---")
    print(result)

    assert result.get("user_id") != None, "user_id가 존재해야합니다."


async def check_email_after_registration(db: AsyncSession, email: str):
    result = await test_email_check(db=db, email=email)
    print("---check_email_after_registration---")
    print(result)
    assert result.get("isUnique") == False, "False로 return 해야합니다."


async def login(db: AsyncSession, form_data: LoginSchema):
    user_info = await test_sign_in(db=db, form_data=form_data)
    print("---login---")
    print(user_info)
    assert user_info.get("user_id") != None, "user_id가 존재해야합니다."
    return user_info


async def check_email_and_name(db: AsyncSession, name: str, email: str):
    result = await test_check_email_and_name(db=db, name=name, email=email)
    print("---check_email_and_name---")
    print(result)

    assert result.get("token") != None, "token이 존재해야합니다."
    return result.get("token")


def convert_token_to_user_id(token: str):
    result = test_convert_token_to_user_id(token=token)
    print("---convert_token_to_user_id---")
    print(result)
    return result


async def update_password(db: AsyncSession, new_password: str, user_id: str, email: str):
    print("---update_password---")

    result = await test_update_password(db=db, new_password=new_password, user_id=user_id)
    user_info = await login(db, LoginSchema(email=email, password=new_password))
    assert user_info.get("user_id") != None, "user_id가 존재해야합니다."
    print("Login Success")
    return result


async def delete_address_force(db: AsyncSession, user_id: str):
    stmt = delete(UserAddressTable).where(UserAddressTable.user_id == user_id)
    await db.execute(stmt)
    await db.commit()
    print("deleting address Success")


async def delete_user(db: AsyncSession, user_id: str):
    stmt = delete(UserTable).where(UserTable.user_id == user_id)
    await db.execute(stmt)
    await db.commit()
    print("deleting user Success")
