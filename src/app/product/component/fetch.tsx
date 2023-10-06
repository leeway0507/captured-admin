import { CreateproductCardProps } from "@/app/types/type";

export const createProduct = async (data: CreateproductCardProps) => {
    const req = await fetch("http://127.0.0.1:8000/api/product/create-product", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return await req.json();
};

export const getProduct = async () => {
    const req = await fetch("http://127.0.0.1:8000/api/product/get-product");
    return await req.json();
};
