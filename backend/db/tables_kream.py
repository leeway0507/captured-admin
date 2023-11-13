from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, DATETIME, BOOLEAN, FLOAT
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class MyBase(Base):
    __abstract__ = True

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}  # type: ignore


class KreamProductCardTable(MyBase):
    __tablename__ = "kream_product_card"

    kream_id = Column(INTEGER, primary_key=True)
    kream_product_img_url = Column(VARCHAR(255))
    kream_product_name = Column(VARCHAR(255))
    brand_name = Column(VARCHAR(255))
    retail_price = Column(INTEGER, nullable=True)
    product_release_date = Column(DATETIME, nullable=True)
    color = Column(VARCHAR(255), nullable=True)
    trading_volume = Column(INTEGER, nullable=True)
    wish = Column(INTEGER)
    review = Column(INTEGER)
    updated_at = Column(DATETIME)

    class Config:
        orm_mode = str


class KreamTradingVolumeTable(MyBase):
    __tablename__ = "kream_trading_volume"

    volume_id = Column(INTEGER, primary_key=True, autoincrement=True)
    kream_id = Column(INTEGER, ForeignKey("kream_product_card.kream_id"))
    kream_product_size = Column(VARCHAR(10))
    price = Column(INTEGER)
    lightening = Column(BOOLEAN)
    trading_at = Column(DATETIME)

    kream_product_card = relationship("KreamProductCardTable")

    class Config:
        orm_mode = str


class KreamBuyAndSellTable(MyBase):
    __tablename__ = "kream_buy_and_sell"
    volume_id = Column(INTEGER, primary_key=True, autoincrement=True)
    kream_id = Column(INTEGER, ForeignKey("kream_product_card.kream_id"))
    kream_product_size = Column(VARCHAR(10))
    buy = Column(INTEGER)
    sell = Column(INTEGER)
    updated_at = Column(DATETIME)

    kream_product_card = relationship("KreamProductCardTable")
    __table_args__ = (
        UniqueConstraint("kream_id", "kream_product_size", name="kream_size_uc"),
    )

    class Config:
        orm_mode = str


class KreamProductIdBridgeTable(MyBase):
    __tablename__ = "kream_product_id_bridge"

    bridge_id = Column(INTEGER, primary_key=True, autoincrement=True)
    product_id = Column(VARCHAR(255))
    kream_id = Column(INTEGER, ForeignKey("kream_product_card.kream_id"), nullable=True)

    __table_args__ = (UniqueConstraint("kream_id", name="kream_id_uc"),)

    kream_product_card = relationship("KreamProductCardTable")

    class Config:
        orm_mode = str
