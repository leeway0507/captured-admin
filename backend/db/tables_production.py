from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, BOOLEAN, DATETIME
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class MyBase(Base):
    __abstract__ = True

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}  # type: ignore


class ProductInfoTable(MyBase):
    __tablename__ = "product_info"

    sku = Column(INTEGER, primary_key=True)
    brand = Column(VARCHAR(50))
    product_name = Column(VARCHAR(255))
    product_id = Column(VARCHAR(255))
    shipping_fee = Column(INTEGER)
    price = Column(INTEGER)
    intl = Column(BOOLEAN)
    search_info = Column(VARCHAR(255))
    color = Column(VARCHAR(50))
    category = Column(VARCHAR(50))
    category_spec = Column(VARCHAR(50))
    img_type = Column(VARCHAR(10))
    price_desc_cursor = Column(VARCHAR(100))
    price_asc_cursor = Column(VARCHAR(100))

    class Config:
        orm_mode = str


class SizeTable(MyBase):
    __tablename__ = "size"
    size_id = Column(INTEGER, primary_key=True, autoincrement=True)
    sku = Column(INTEGER, ForeignKey("product_info.sku"), nullable=False)
    size = Column(VARCHAR(50), nullable=False)
    available = Column(BOOLEAN, nullable=False, default=True)
    updated_at = Column(
        DATETIME,
        nullable=False,
    )
    product = relationship("ProductInfoTable")

    __table_args__ = (UniqueConstraint("sku", "size", name="_sku_size_uc"),)

    class Config:
        orm_mode = str


class UserTable(MyBase):
    __tablename__ = "user"

    user_id = Column(VARCHAR(50), primary_key=True)
    email = Column(VARCHAR(255), nullable=True, unique=True)
    password = Column(VARCHAR(255), nullable=True)
    kr_name = Column(VARCHAR(30), nullable=False)
    email_verification = Column(BOOLEAN, nullable=False, default=False)
    register_at = Column(DATETIME, nullable=False)
    sign_up_type = Column(VARCHAR(20), nullable=False)

    class Config:
        orm_mode = str


class UserAddressTable(MyBase):
    __tablename__ = "user_address"
    address_id = Column(VARCHAR(255), primary_key=True)
    user_id = Column(VARCHAR(50), ForeignKey("user.user_id"), nullable=False)
    kr_name = Column(VARCHAR(30), nullable=False)
    en_name = Column(VARCHAR(30), nullable=False)
    custom_id = Column(VARCHAR(50), nullable=False)
    phone = Column(VARCHAR(20), nullable=False)
    kr_address = Column(VARCHAR(255), nullable=False)
    kr_address_detail = Column(VARCHAR(255), nullable=False)
    en_address = Column(VARCHAR(255), nullable=False)
    en_address_detail = Column(VARCHAR(255), nullable=False)
    permanent = Column(BOOLEAN, nullable=False, default=False)

    user = relationship("UserTable")

    class Config:
        orm_mode = str


class OrderHistoryTable(MyBase):
    __tablename__ = "order_history"
    order_id = Column(VARCHAR(255), primary_key=True)
    user_id = Column(VARCHAR(50), ForeignKey("user.user_id"), nullable=False)
    address_id = Column(VARCHAR(255), ForeignKey("user_address.address_id"), nullable=False)
    ordered_at = Column(DATETIME, nullable=False)
    user_order_number = Column(INTEGER, nullable=False)
    order_status = Column(VARCHAR(50), nullable=False)
    order_total_price = Column(INTEGER, nullable=False)
    payment_method = Column(VARCHAR(50), nullable=False)
    payment_status = Column(VARCHAR(50), nullable=False)
    payment_info = Column(VARCHAR(255), nullable=True)
    payment_key = Column(VARCHAR(255), nullable=False)

    user = relationship("UserTable")
    address = relationship("UserAddressTable")

    class Config:
        orm_mode = str


class OrderRowTable(MyBase):
    __tablename__ = "order_row"
    order_row_id = Column(INTEGER, primary_key=True, autoincrement=True)
    order_id = Column(VARCHAR(255), ForeignKey("order_history.order_id"), nullable=False)
    sku = Column(INTEGER, ForeignKey("product_info.sku"), nullable=False)
    size = Column(VARCHAR(20), nullable=False)
    quantity = Column(INTEGER, nullable=False)
    delivery_status = Column(VARCHAR(10), nullable=False)
    delivery_company = Column(VARCHAR(30), nullable=True)
    delivery_number = Column(VARCHAR(50), nullable=True)

    order = relationship("OrderHistoryTable")
    product = relationship("ProductInfoTable")

    class Config:
        orm_mode = str
