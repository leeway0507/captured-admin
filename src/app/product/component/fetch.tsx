import { CreateproductCardProps } from "@/app/types/type";

export const getProduct = async () => {
    const req = await fetch("http://127.0.0.1:8000/api/admin/get-category");
    return await req.json();
};

export const createProduct = async (data: CreateproductCardProps) => {
    const req = await fetch("http://127.0.0.1:8000/api/admin/create-product", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return await req.json();
};

export const updateProduct = async (data: CreateproductCardProps) => {
    const req = await fetch("http://127.0.0.1:8000/api/admin/update-product", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return await req.json();
};
