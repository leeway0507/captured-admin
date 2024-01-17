import { CreateproductCardProps } from "@/app/types/type";

export const getProductData = async (page: number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/table/production-table`;
    const queryParams = new URLSearchParams({
        page: page.toString(),
    });

    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};

export const updateProductData = async (data: CreateproductCardProps) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/table/production-table`;
    const req = await fetch(url, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return { status: req.status, data: await req.json() };
};

export const patchProductData = async (sku: number, column: string, value: any) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/table/production-table`;
    const queryParams = new URLSearchParams({
        sku: sku.toString(),
        column,
        value,
    });

    const res = await fetch(url + "?" + queryParams, { method: "PATCH" });
    return { status: res.status, data: await res.json() };
};

export const deleteProductData = async (sku: number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/table/production-table/${sku}`;

    const res = await fetch(url, { method: "DELETE" });
    return { status: res.status, data: await res.json() };
};

export const uploadImageToS3 = async (sku: number) => {
    const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/production/s3/upload-product-image-to-s3?sku=${sku}`
    );
    return { status: res.status, data: await res.json() };
};
