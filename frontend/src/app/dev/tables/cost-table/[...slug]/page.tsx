import { getCostTableDataSet, getProductInfoFromProduction } from "../fetch";
import { CostTable } from "./table/table";
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

    const costTableDataSet = await getCostTableDataSet(searchTypeDecoded, valueDecoded);
    const productInfo = await getProductInfoFromProduction();

    return (
        <>
            <CostTable costTableDataSet={costTableDataSet.data} productInfo={productInfo.data} />
        </>
    );
}
