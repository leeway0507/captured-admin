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

export const getShopPageList = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-shop-product-page`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const InitshopCardPage = async (searchType: string, content: string, numProcess: number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/init-shop-product-card-page`;

    const queryParams = new URLSearchParams({
        searchType,
        content,
        numProcess: numProcess.toString(),
    });

    const res = await fetch(url + "?" + queryParams);

    return { status: res.status, data: await res.json() };
};
export const CloseCustomPageBrowser = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/close-custom-page`;
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

export const getScrapList = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-scrap-list`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const getScrapPageList = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-scrap-page-list`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const getProductListResult = async (scrapName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-product-list-result`;
    const queryParams = new URLSearchParams({
        scrapName,
    });
    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};

export const getProductPageResult = async (scrapName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-product-page-result`;
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

export const loadScrapedBrandName = async (shopName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-scraped-brand-name`;
    const queryParams = new URLSearchParams({
        shopName,
    });
    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};

export const insertScrapPageToDB = async (scrapDate: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/db/upsert-shop-product-size-table`;
    const queryParams = new URLSearchParams({
        scrapDate,
    });
    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};

export const deleteScrapList = async (scrapName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/delete-product-list-result`;
    const queryParams = new URLSearchParams({
        scrapName,
    });
    const res = await fetch(url + "?" + queryParams, {
        method: "DELETE",
    });
    return { status: res.status, data: await res.json() };
};
