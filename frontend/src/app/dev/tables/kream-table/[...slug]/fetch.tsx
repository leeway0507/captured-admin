export const getKreamProductCardList = async (searchType: string, content: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/get-kream-product-detail-list`;
    const queryParams = new URLSearchParams({
        searchType,
        content,
    });

    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};

export const getKreamProductSizeInfo = async (searchType: string, content: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/kream/get-kream-product-size-info`;
    const queryParams = new URLSearchParams({
        searchType,
        content,
    });
    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};
