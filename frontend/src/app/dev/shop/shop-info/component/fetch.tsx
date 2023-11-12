import { shopInfoProps } from "../../type";

export const getShopInfo = async () => {
    const req = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/db/get-shop-info`);
    return { status: req.status, data: await req.json() };
};

export const createShopInfo = async (data: shopInfoProps) => {
    const req = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/db/upsert-shop-info`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return { status: req.status, data: await req.json() };
};
