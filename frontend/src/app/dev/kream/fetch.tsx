export const InitProductCardList = async (brandName: string, maxScroll: Number, minWish: Number, minVolume: Number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/scrap-platform-list`;

    const queryParams = new URLSearchParams({
        brandName: brandName,
        maxScroll: maxScroll.toString(),
        minWish: minWish.toString(),
        minVolume: minVolume.toString(),
    });

    const res = await fetch(url + "?" + queryParams);

    return { status: res.status, data: await res.json() };
};

export const InitProductPage = async (searchType: string, value: string, numProcess: Number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/scrap-platform-page`;

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

export async function getScrapList() {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/get-platform-list-report-list`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
}

export async function getScrapListReport(scrapName: string) {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/get-platform-list-report?scrapName=${scrapName}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
}

export async function getScrapPageReport(scrapName: string) {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/get-platform-page-report?scrapName=${scrapName}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
}

export async function getScrapPage() {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/get-platform-page-report-list`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
}

export async function insertListScrapToDB(platformType: string, scrapTime: string) {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/db/update-scrap-kream-product-card-list`;

    const queryParams = new URLSearchParams({
        platformType,
        scrapTime,
    });

    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
}

export async function insertPageScrapToDB(searchValue: string, scrapTime: string) {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/db/update-all-detail-kream-to-db`;

    const queryParams = new URLSearchParams({
        searchValue,
        scrapTime,
    });

    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
}

export async function RestartSavingCreatelog(scrapName: string) {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/restart-saving-create-log?scrapName=${scrapName}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
}

export async function RestartSavingLastScrapedFiles(brandName: string) {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/restart-saving-last-scraped-files?brandName=${brandName}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
}
