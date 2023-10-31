from sqlalchemy.ext.asyncio import AsyncSession
from router.mypage import utils as mypage_utils
from router.auth import utils as auth_utils
from model.db_model import UserAddressSchema, UserAddressInDBSchema, UserSchema
from model.auth_model import TokenData


async def test_get_address(db: AsyncSession, user: TokenData):
    """주소 목록 조회"""
    return await mypage_utils.get_user_address(db, user)


async def test_get_address_info_by_id(address_id: str, db: AsyncSession):
    """주소 상세 조회"""
    return await mypage_utils.get_user_address_info(db, address_id)


async def test_create_address(db: AsyncSession, user: TokenData, address: UserAddressSchema):
    """주소 생성"""
    address.address_id = await mypage_utils.create_new_address_id(db, user.user_id)
    new_address = UserAddressInDBSchema(user_id=user.user_id, **address.model_dump())

    if await mypage_utils.create_user_address(db, new_address):
        return {"message": "success"}
    else:
        raise Exception("주소 등록에 실패했습니다. 다시 시도해주세요.")


async def test_update_address(
    db: AsyncSession, user: TokenData, updated_address: UserAddressSchema
):
    """주소 수정"""

    assert updated_address.address_id is not None, "address_id가 존재해야합니다."

    user_address_db = UserAddressInDBSchema(user_id=user.user_id, **updated_address.model_dump())
    if await mypage_utils.update_user_address(db, user_address_db):
        return {"message": "success"}
    else:
        raise Exception("주소 업데이트에 실패했습니다. 다시 시도해주세요.")


async def test_delete_address(db: AsyncSession, address_id: str):
    """주소 삭제"""
    if await mypage_utils.delete_user_address(db, address_id):
        return {"message": "success"}
    else:
        raise Exception("주소 삭제에 실패했습니다. 다시 시도해주세요.")
