import { CreateproductCardProps } from "@/app/types/type";

export const getProduct = async () => {
    const req = await fetch(`${process.env.NEXT_PUBLIC_FRONTEND_URL}/api/production/get-category`);
    return await req.json();
};

export const createProduct = async (data: CreateproductCardProps) => {
    const req = await fetch(`${process.env.NEXT_PUBLIC_FRONTEND_URL}/api/production/create-product`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return await req.json();
};

export const updateProduct = async (data: CreateproductCardProps) => {
    const req = await fetch(`${process.env.NEXT_PUBLIC_FRONTEND_URL}/api/production/update-product`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return await req.json();
};
