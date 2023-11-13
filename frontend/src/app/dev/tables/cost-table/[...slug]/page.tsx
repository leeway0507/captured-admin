import Main from "./main";
import { getShopInfoByName, getProductCardList } from "./fetch";

export default async function Page({
    params,
    searchParams,
}: {
    params: { slug: string[] };
    searchParams: { [key: string]: string | undefined };
}) {
    const [shopName, brandName] = params.slug;

    const shopNameDecoded = decodeURIComponent(shopName);
    const brandNameDecoded = decodeURIComponent(brandName);
    const shopInfo = await getShopInfoByName(shopNameDecoded);
    const productCardList = await getProductCardList(shopNameDecoded, brandNameDecoded);

    return (
        <>
            <Main shopInfo={shopInfo.data} productCardList={productCardList.data} />
        </>
    );
}
