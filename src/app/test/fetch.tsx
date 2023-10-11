import { CreateproductCardProps } from "../types/type";

export const getProduct = async () => {
    const req = await fetch("http://127.0.0.1:8000/api/admin/get-category");
    const data: CreateproductCardProps[] = await req.json();
    return data;
};

export const getProductByCursor = async (sku: number, page: number) => {
    const req = await fetch(`http://127.0.0.1:8000/api/admin/get-cursor-test?sku=${sku}&page=${page}`);
    const data: CreateproductCardProps[] = await req.json();
    return data;
};
