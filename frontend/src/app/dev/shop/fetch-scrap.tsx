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

export const ScrapShopPage = async (searchType: string, value: string | Object, numProcess: number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/shop/page/scrap`;

    const stringValue = typeof value === "object" ? JSON.stringify(value) : value;

    const queryParams = new URLSearchParams({
        searchType,
        value: stringValue,
        numProcess: numProcess.toString(),
    });

    const res = await fetch(url + "?" + queryParams, {
        method: "GET", // Specify the HTTP method (GET in this case)
        headers: {
            "Content-Type": "application/json", // Add this header if necessary
        },
    });

    return { status: res.status, data: await res.json() };
};

export const loadShopListName = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/shop/list/sub_scraper_list`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const loadShopListBrandName = async (shopName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/shop/list/sub_scraper_brand/${shopName}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const loadShopPageName = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/shop/page/sub_scraper_list`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const loadShopPageBrandName = async (shopName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/shop/page/sub_scraper_brand/${shopName}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const CloseCustomPageBrowser = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/close-custom-page`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};
