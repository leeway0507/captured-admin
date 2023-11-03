export const getOrderRow = async () => {
    const req = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/production/get-order-row`);
    return await req.json();
};

export const getOrderHistory = async () => {
    const req = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/production/get-order-history`);
    return await req.json();
};
