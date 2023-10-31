from model.db_model import (
    ProductInfoSchema,
    UserAddressSchema,
    OrderHistoryRequestSchema,
    OrderRowSchmea,
    OrderHistoryInDBSchema,
    OrderRowInDBSchmea,
)
from model.product_model import RequestFilterSchema
from model.registration_model import EmailRegistrationSchema


def get_product_info():
    return ProductInfoSchema(
        sku=0,
        brand="nike",
        product_name="nike air force",
        product_id="gy7386",
        size=None,
        price=100000,
        shipping_fee=2000,
        intl=True,
        color="['black']",
        category="신발",
        category_spec="스니커즈",
        img_type="jpg",
    )


def get_filter():
    return RequestFilterSchema(
        sort_by="",
        category="",
        category_spec="",
        brand="",
        intl="",
        price="",
        size_array="",
    )


def get_register_info():
    return EmailRegistrationSchema(
        email="test@example.com",
        password="test123",
        kr_name="captured",
        sign_up_type="email",
    )


def get_address_info():
    return UserAddressSchema(
        kr_name="captured",
        en_name="캡쳐드",
        custom_id="p2929293929",
        phone="01012345678",
        kr_address="서울",
        kr_address_detail="101",
        en_address="seoul",
        en_address_detail="101",
    )


def get_new_address_info():
    return UserAddressSchema(
        kr_name="capturedV2",
        en_name="캡쳐드V2",
        custom_id="p2929293929",
        phone="01012345678",
        kr_address="서울V2",
        kr_address_detail="101V2",
        en_address="seoulV2",
        en_address_detail="101V2",
    )


def get_order_history_info():
    return OrderHistoryRequestSchema(
        user_id="",
        address_id="",
        order_total_price=100000,
        payment_method="",
        payment_info="",
    )


def get_order_rows():
    return [
        OrderRowSchmea(sku=1, size="225", quantity=1),
        OrderRowSchmea(sku=1, size="230", quantity=1),
    ]
