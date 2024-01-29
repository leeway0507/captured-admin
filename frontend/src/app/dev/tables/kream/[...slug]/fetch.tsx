export const getKreamProdCard = async (productId: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/table/kream/product/productId/${productId}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const getKreamProdCardByBrandName = async (brandName: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/table/kream/product/brandName/${brandName}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};

export const getKreamMarketPrice = async (productId: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/table/kream/market-price/${productId}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};
