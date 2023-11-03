from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, DATETIME, BOOLEAN,FLOAT
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class MyBase(Base):
    __abstract__ = True

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}  # type: ignore


class ShopInfoTable(MyBase):
    __tablename__ = "shop_info"

    shop_name = Column(VARCHAR(100), primary_key=True)
    shop_url = Column(VARCHAR(255))
    tax_reduction_rate = Column(FLOAT,nullable=True)
    del_agc_tax_reduction_rate = Column(FLOAT,nullable=True)
    dome_ship_price = Column(INTEGER,nullable=True)
    intl_ship_price = Column(INTEGER,nullable=True)
    from_us_shipping = Column(BOOLEAN,nullable=True)
    is_ddp = Column(BOOLEAN,nullable=True)
    updated_at = Column(DATETIME)


class ShopInBrandTable(MyBase):
    __tablename__ = "shop_in_brand"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    shop_name = Column(VARCHAR(100), ForeignKey("shop_info.shop_name"))
    brand_name = Column(VARCHAR(100))
    brand_url = Column(VARCHAR(255))
    updated_at = Column(DATETIME)

    __table_args__ = (UniqueConstraint("brand_name", name="brand_name_uc"),)
    shop_info = relationship("ShopInfoTable")


class ShopProductCardTable(MyBase):
    __tablename__ = "shop_product_card"
    
    shop_product_card_id = Column(INTEGER, primary_key=True, autoincrement=True)
    shop_product_name = Column(VARCHAR(255))
    shop_name = Column(VARCHAR(100), ForeignKey("shop_info.shop_name"))
    brand_name = Column(VARCHAR(100), ForeignKey("shop_in_brand.brand_name"))
    product_id = Column(VARCHAR(255), index=True)
    search_keyword = Column(VARCHAR(255))
    shop_product_img_url = Column(VARCHAR(255))
    product_url = Column(VARCHAR(255))
    kor_price = Column(INTEGER)
    us_price = Column(FLOAT)
    original_price_currency = Column(VARCHAR(10))
    original_price = Column(FLOAT)
    sold_out = Column(BOOLEAN)
    updated_at = Column(DATETIME)

    __table_args__ = (UniqueConstraint("shop_product_name", name="shop_product_name_uc"),)


    shop_info = relationship("ShopInfoTable")
    shop_in_brand = relationship("ShopInBrandTable")

class ShopProductSizeTable(MyBase) :
    __tablename__ = "shop_product_size"

    shop_product_size_id = Column(INTEGER, primary_key=True, autoincrement=True)
    shop_product_card_id=Column(INTEGER,ForeignKey("shop_product_card.shop_product_card_id"))
    shop_product_size = Column(VARCHAR(100))
    kor_product_size = Column(VARCHAR(100))
    available = Column(BOOLEAN)
    updated_at = Column(DATETIME)

    shop_product_card = relationship("ShopProductCardTable")
