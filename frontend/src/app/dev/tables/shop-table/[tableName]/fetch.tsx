export const getCostTableBrandNameData = async (value: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/table/get-cost-table-brand-name-data`;
    const queryParams = new URLSearchParams({
        value,
    });

    const res = await fetch(url + "?" + queryParams, { cache: "no-cache" });
    return { status: res.status, data: await res.json() };
};

export const getCostTableShopNameData = async (value: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/table/get-cost-table-shop-name-data`;
    const queryParams = new URLSearchParams({
        value,
    });

    const res = await fetch(url + "?" + queryParams, { cache: "no-cache" });
    return { status: res.status, data: await res.json() };
};

export const getCandidateTableBrandNameData = async (value: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/table/get-candidate-table-brand-name-data`;
    const queryParams = new URLSearchParams({
        value,
    });
    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};
export const getCandidateTableShopNameData = async (value: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/table/get-candidate-table-shop-name-data`;
    const queryParams = new URLSearchParams({
        value,
    });
    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};

export const updateShopProductCard = async (shopProductCardId: number, value: object) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/db/update-shop-product-card-for-cost-table`;
    const body = {
        shopProductCardId,
        value,
    };
    const res = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });
    return { status: res.status, data: await res.json() };
};

export const getProductInfoFromProduction = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/production/get-product-info-for-cost-product`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const getKreamColor = async (productId: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/get-product-color-for-registraion`;
    const queryParams = new URLSearchParams({
        productId,
    });

    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};
export const getShopProductSizeTableData = async (productId: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/db/get-shop-product-size-table-data`;
    const queryParams = new URLSearchParams({
        productId,
    });

    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};
