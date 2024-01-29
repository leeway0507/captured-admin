//list
export const getShopListReportAll = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/shop/list/report/list`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};
export const getShopListReportItem = async (reportName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/shop/list/report/item/${reportName}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const insertShopListData = async (scrapName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/shop/list/sync_db/${scrapName}`;
    const res = await fetch(url, { method: "POST" });
    return { status: res.status, data: await res.json() };
};

//page
export const getShopPageReportAll = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/shop/page/report/list`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};
export const getShopPageReportItem = async (reportName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/shop/page/report/item/${reportName}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const insertShopPageData = async (scrapName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/shop/page/sync_db/${scrapName}`;
    const res = await fetch(url, { method: "POST" });
    return { status: res.status, data: await res.json() };
};
