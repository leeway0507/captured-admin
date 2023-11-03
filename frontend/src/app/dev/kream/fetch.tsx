export const InitProductCardList = async (brandName: string, maxScroll: Number, minWish: Number, minVolume: Number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/init-product-card-list`;

    const queryParams = new URLSearchParams({
        brandName: brandName,
        maxScroll: maxScroll.toString(),
        minWish: minWish.toString(),
        minVolume: minVolume.toString(),
    });

    const res = await fetch(url + "?" + queryParams);

    return { status: res.status, data: await res.json() };
};

export const InitProductDetail = async (brandName: string, numProcess: Number, kreamIds: string = "") => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/init-product-detail`;

    const queryParams = new URLSearchParams({
        brandName: brandName,
        numProcess: numProcess.toString(),
        kreamIds: kreamIds,
    });

    const res = await fetch(url + "?" + queryParams);

    return { status: res.status, data: await res.json() };
};

export const ReloadBrowser = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/reload-kream-page`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export async function getScraptResult(scrapName: string) {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/get-scrap-result?scrapName=${scrapName}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
}

export async function getScraptList() {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/get-scrap-list`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
}
