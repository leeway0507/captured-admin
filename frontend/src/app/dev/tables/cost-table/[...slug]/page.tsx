import { getCostTableDataSet, getProductInfoFromProduction } from "../fetch";
import { CostTable } from "./table/cost-table";
export default async function Page({
    params,
    searchParams,
}: {
    params: { slug: string[] };
    searchParams: { [key: string]: string | undefined };
}) {
    const [searchTypeEncoded, valueEncoded] = params.slug;

    const searchType = decodeURIComponent(searchTypeEncoded);
    var value = decodeURIComponent(valueEncoded).replaceAll("-", " ");

    if (searchType === "brandName") {
        value = value.replaceAll(" ", "_");
    }

    const costTableDataSet = await getCostTableDataSet(searchType, value);
    const productInfo = await getProductInfoFromProduction();

    return (
        <>
            <CostTable costTableDataSet={costTableDataSet.data} productInfo={productInfo.data} />
        </>
    );
}
