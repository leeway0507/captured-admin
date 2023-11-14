export const getProductCardListForCostTable = async (searchType: string, value: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/dev/shop/get-shop-product-list-for-cost-table`;
    const queryParams = new URLSearchParams({
        searchType,
        value,
    });

    const res = await fetch(url + "?" + queryParams);
    return { status: res.status, data: await res.json() };
};
