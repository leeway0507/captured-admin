export interface CreateproductCardProps {
    sku?: number;
    brand: string;
    productName: string;
    productId: string;
    size: string;
    price: string;
    shippingFee: string;
    intl: string;
    color: string;
    category: string;
    imgType: string;
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
    orderDate: string;
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
