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

export const getShopInfoByName = async (shopName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-shop-info`;
    const queryParams = new URLSearchParams({
        shopName,
    });
    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};

export const getProductCardList = async (shopName: string, brandName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-shop-product-list`;
    const queryParams = new URLSearchParams({
        shopName,
        brandName,
    });

    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};

export const getBuyingCurrency = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-buying-currency`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const getCustomCurrency = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-buying-currency`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const updateCandidate = async (shopProductCardId: number, candidate: number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/db/update-candidate-status`;
    const queryParams = new URLSearchParams({
        shopProductCardId: shopProductCardId.toString(),
        candidate: candidate.toString(),
    });

    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};
