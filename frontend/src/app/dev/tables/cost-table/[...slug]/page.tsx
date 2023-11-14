import { getProductCardListForCostTable } from "../fetch";
import Main from "./main";
import { productCardProps } from "./table/table";

export default async function Page({
    params,
    searchParams,
}: {
    params: { slug: string[] };
    searchParams: { [key: string]: string | undefined };
}) {
    const [searchType, value] = params.slug;

    const searchTypeDecoded = decodeURIComponent(searchType);
    var valueDecoded = decodeURIComponent(value).replaceAll("-", " ");

    if (searchTypeDecoded === "brandName") {
        valueDecoded = valueDecoded.replaceAll(" ", "_");
    }

    const productCardList = await getProductCardListForCostTable(searchTypeDecoded, valueDecoded);

    return (
        <>
            <Main productCardList={productCardList.data} />
        </>
    );
}
