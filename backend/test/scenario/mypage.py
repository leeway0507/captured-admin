from test_module.mypage import *
from variables import get_new_address_info, get_register_info, get_address_info
from db.tables import UserAddressTable
from scenario.auth import login, register_user_and_address, delete_user, delete_address_force
from model.auth_model import LoginSchema
from model.db_model import UserAddressSchema
from sqlalchemy.ext.asyncio import AsyncSession


async def mypage_scenario(db):
    new_address_info = get_new_address_info()
    register_info = get_register_info()
    form_data = LoginSchema(email=register_info.email, password=register_info.password)

    # 주소 조회(회원가입 시 생성)
    # 주소 업데이트
    # 주소 생성
    # 최종 삭제

    print("----------mypage_scenario 시작----------")

    # 유저 생성
    try:
        user_info = await login(db=db, form_data=form_data)
    except:
        await register_user_and_address(
            db=db, register_info=register_info, address_info=get_address_info()
        )
        user_info = await login(db=db, form_data=form_data)

    user = TokenData(**user_info)

    address = await get_address(db=db, user=user)
    await update_address(db=db, user=user, address=address[0])
    new_address = await create_address(db=db, user=user, address=new_address_info)
    await delete_address(db=db, user=user, address_id=new_address[-1].address_id)  # type: ignore
    # 종료
    await delete_address_force(db=db, user_id=user.user_id)
    await delete_user(db=db, user_id=user.user_id)
    print("----------mypage_scenario 종료----------")


# Part --------------------------------------------------------------


async def get_address(db: AsyncSession, user: TokenData):
    print("---get_address---")
    result = await test_get_address(db=db, user=user)
    print(result)
    assert len(result) >= 1, "주소가 존재해야합니다."
    return result


async def create_address(db: AsyncSession, user: TokenData, address: UserAddressSchema):
    print("---create_address---")
    result = await test_create_address(db, user, address)
    print(result)
    check_address = await test_get_address(db=db, user=user)
    print(check_address)
    assert check_address[-1] == address, "생성된 주소와 조회된 주소가 같아야합니다."
    return check_address


async def update_address(db: AsyncSession, user: TokenData, address: UserAddressSchema):
    print("---update_address---")
    address.custom_id = "p99999999"
    address.kr_name = "캡처드업데이트"
    result = await test_update_address(db=db, user=user, updated_address=address)
    print(result)
    check_address = await test_get_address(db=db, user=user)
    print(check_address)
    assert check_address[0] == address, "업데이트 된 주소와 조회된 주소가 같아야합니다."


async def delete_address(db: AsyncSession, user: TokenData, address_id: str):
    print("---delete_address---")
    print(address_id)
    result = await test_delete_address(db=db, address_id=address_id)
    print("delete address_id:", result)
    check_address = await test_get_address(db=db, user=user)
    print("rest address_id:", check_address[-1].address_id)
    assert check_address[-1].address_id != address_id, "주소가 삭제되어야합니다."
