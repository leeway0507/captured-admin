export const getCostTableDataSet = async (searchType: string, value: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-shop-product-list-for-cost-table`;
    const queryParams = new URLSearchParams({
        searchType,
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
        method: "POST",
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
