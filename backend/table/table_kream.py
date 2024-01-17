async def get_shop_product_size_table_data(db: AsyncSession, product_id):
    product_id_list = product_id.split(",")

    stmt = (
        select(ShopProductSizeTable)
        .join(ShopProductCardTable)
        .where(ShopProductCardTable.product_id.in_(product_id_list))
    )
    size_rows = await db.execute(stmt)
    size_rows = size_rows.scalars().all()

    stmt = select(ShopProductCardTable).where(
        ShopProductCardTable.product_id.in_(product_id_list)
    )
    prod_rows = await db.execute(stmt)
    prod_rows = prod_rows.scalars().all()
    return {
        "sizeInfo": [ShopProductSizeSchema(**row.to_dict()) for row in size_rows],
        "productInfo": [ShopProductCardSchema(**row.to_dict()) for row in prod_rows],
    }
