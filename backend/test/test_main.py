import sys

sys.path.append("/Users/yangwoolee/repo/captured/main/backend")
import asyncio
from scenario import product_scenario, auth_scenario, mypage_scenario, order_scenario
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from db.tables import Base


async def test_product_crud():
    db_engine = create_async_engine(f"mysql+aiomysql://root@localhost:3306/captured_test")
    session_local = sessionmaker(bind=db_engine, class_=AsyncSession)  # type: ignore
    session = session_local()

    # table 생성
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # type: ignore

    # 시나리오 시작
    await product_scenario(db=session)
    await auth_scenario(db=session)
    await mypage_scenario(db=session)
    await order_scenario(db=session)

    # table 제거
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # type: ignore

    await db_engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_product_crud(), debug=False)
