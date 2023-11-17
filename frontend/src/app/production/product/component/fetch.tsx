import { CreateproductCardProps } from "@/app/types/type";

export const getProduct = async (page: number, limit: number = 50) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/production/get-category`;
    const queryParams = new URLSearchParams({
        page: page.toString(),
        limit: limit.toString(),
    });

    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};

export const createProduct = async (data: CreateproductCardProps) => {
    const req = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/production/create-product`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return { status: req.status, data: await req.json() };
};

export const updateProduct = async (data: CreateproductCardProps) => {
    const req = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/production/update-product`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return { status: req.status, data: await req.json() };
};

export const updateProductDeploy = async (sku: number, status: number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/production/update-product-deploy-status`;
    const queryParams = new URLSearchParams({
        sku: sku.toString(),
        status: status.toString(),
    });

    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};

export const deleteProduct = async (sku: number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/production/delete-product`;
    const queryParams = new URLSearchParams({
        sku: sku.toString(),
    });

    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};
