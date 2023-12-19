import {
    getCostTableBrandNameData,
    getCostTableShopNameData,
    getCandidateTableBrandNameData,
    getCandidateTableShopNameData,
} from "../fetch";
import { CostTable } from "./cost-table";

const getData = async (tableType: string, searchType: string, value: string) => {
    switch (tableType) {
        case "candidate-table":
            if (searchType === "brand-name") {
                value = value.replaceAll(" ", "_");
                return await getCandidateTableBrandNameData(value);
            }
            if (searchType === "shop-name") {
                return await getCandidateTableShopNameData(value);
            }

        case "cost-table":
            if (searchType === "brand-name") {
                value = value.replaceAll(" ", "_");
                return await getCostTableBrandNameData(value);
            }
            if (searchType === "shop-name") {
                return await getCostTableShopNameData(value);
            }
        default:
            return { status: 404, data: [] };
    }
};
export default async function Page({
    params,
    searchParams,
}: {
    params: { slug: string[] };
    searchParams: { [key: string]: string | undefined };
}) {
    const { tableType, searchType, value } = searchParams;
    const costTableDataSet = await getData(tableType!, searchType!, value!);

    return <CostTable costTableDataSet={costTableDataSet.data} />;
}
