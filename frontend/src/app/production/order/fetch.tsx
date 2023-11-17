export const getOrderHistory = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/production/get-order-history`;

    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};
