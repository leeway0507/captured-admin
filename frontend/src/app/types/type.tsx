export interface CreateproductCardProps {
    sku?: number;
    brand: string;
    korBrand: string;
    productName: string;
    korProductName: string;
    productId: string;
    price: number;
    shippingFee: number;
    intl: boolean;
    color: string;
    category: string;
    categorySpec: string;
    imgType: string;
    deploy?: number;
    searchInfo?: string;
}
export interface productCardProps {
    shopProductCardId: number;
    shopProductName: string;
    shopProductImgUrl: string;
    productUrl: string;
    shopName: string;
    brandName: string;
    productId: string;
    korPrice: number;
    usPrice: number;
    originalPriceCurrency: string;
    originalPrice: number;
    soldOut: boolean;
    candidate: number;
    updatedAt: string;
    coupon: number;
}
export interface userAddressProps {
    addressId: string;
    krName: string;
    enName: string;
    customId: string;
    phone: string;
    krAddress: string;
    enAddress: string;
    krAddressDetail: string;
    enAddressDetail: string;
}
export interface setUserAddressProps extends userAddressProps {
    setAddressId: (v: string) => void;
    setKrName: (v: string) => void;
    setEnName: (v: string) => void;
    setCustomId: (v: string) => void;
    setPhone: (v: string) => void;
    setKrAddress: (v: string) => void;
    setEnAddress: (v: string) => void;
    setKrAddressDetail: (v: string) => void;
    setEnAddressDetail: (v: string) => void;
}

export interface userProps {
    name: string;
    email: string;
    password: string;
}

export interface orderHistoryProps {
    orderId: string;
    orderNumber: string;
    orderedAt: string;
    orderStatus: string;
    orderPrice: string;
}

export interface orderRowProps {
    orderNum: number;
    order_id: string;
    sku: number;
    size: string;
    quantity: number;
    deliveryStatus: string;
    deliveryNumber: string;
    deliveryCompany: string;
}

export interface orderHistoryProps {
    userId: number;
    orderDate: string;
    addressId: string;
    orderTotalPrice: number;
    paymentMethod: string;
    paymentInfo: string;
    orderId: string;
    userOrderNumber: number;
    orderStatus: string;
    paymentStatus: string;
}

export interface orderRowProps {
    sku: number;
    size: string;
    quantity: number;
    orderRowId: number;
    orderId: string;
    deliveryStatus: string;
    deliveryCompany: string;
    deliveryNumber: string;
}
