export const ScrapPlatformList = async (brandName: string, maxScroll: Number, minWish: Number, minVolume: Number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/platform/list/scrap`;

    const queryParams = new URLSearchParams({
        brandName: brandName,
        maxScroll: maxScroll.toString(),
        minVolume: minVolume.toString(),
        minWish: minWish.toString(),
    });

    const res = await fetch(url + "?" + queryParams);

    return { status: res.status, data: await res.json() };
};

export const ScrapPlatformPage = async (searchType: string, value: string, numProcess: Number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/platform/page/scrap`;

    const queryParams = new URLSearchParams({
        searchType,
        value,
        numProcess: numProcess.toString(),
    });

    const res = await fetch(url + "?" + queryParams);

    return { status: res.status, data: await res.json() };
};

export const CloseKreamBrowser = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/close-kream-page`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};
