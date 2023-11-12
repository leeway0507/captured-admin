export const InitshopCardList = async (shopName: string, brandName: string, numProcess: number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/init-shop-product-card-list`;

    const queryParams = new URLSearchParams({
        shopName,
        brandName,
        numProcess: numProcess.toString(),
    });

    const res = await fetch(url + "?" + queryParams);

    return { status: res.status, data: await res.json() };
};

export const ReloadBrowser = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/reload-kream-page`;
    const res = await fetch(url);
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

export const getScraptList = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-scrap-list`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const getScraptResult = async (scrapName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-scrap-data`;
    const queryParams = new URLSearchParams({
        scrapName,
    });
    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};

export const insertScarpToDB = async (scrapName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/db/update-last-scrap-shop-product-card-list`;
    const queryParams = new URLSearchParams({
        scrapName,
    });
    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};
