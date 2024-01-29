//list
export const getPlatformListReportAll = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/platform/list/report/list`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};
export const getPlatformListReportItem = async (reportName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/platform/list/report/item/${reportName}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const insertPlatformListData = async (scrapTime: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/platform/list/sync_db/${scrapTime}`;
    const res = await fetch(url, { method: "POST" });
    return { status: res.status, data: await res.json() };
};

//page
export const getPlatformPageReportAll = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/platform/page/report/list`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};
export const getPlatformPageReportItem = async (reportName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/platform/page/report/item/${reportName}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const insertPlatformPageData = async (scrapType: string, scrapTime: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/platform/page/sync_db/${scrapTime}`;
    const res = await fetch(url, { method: "POST" });
    return { status: res.status, data: await res.json() };
};
