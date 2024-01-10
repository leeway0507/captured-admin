export const ScrapShopList = async (shopName: string, brandName: string, numProcess: number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/shop/list/scrap`;

    const queryParams = new URLSearchParams({
        shopName,
        brandName,
        numProcess: numProcess.toString(),
    });

    const res = await fetch(url + "?" + queryParams);

    return { status: res.status, data: await res.json() };
};

export const ScrapShopPage = async (searchType: string, value: string, numProcess: number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/shop/page/scrap`;

    const queryParams = new URLSearchParams({
        searchType,
        value,
        numProcess: numProcess.toString(),
    });

    const res = await fetch(url + "?" + queryParams);

    return { status: res.status, data: await res.json() };
};

export const loadShopName = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-shop-name`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const loadBrandName = async (shopName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-brand-name`;
    const queryParams = new URLSearchParams({
        shopName,
    });
    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};

export const getShopPageList = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-shop-product-page`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const CloseCustomPageBrowser = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/close-custom-page`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};
