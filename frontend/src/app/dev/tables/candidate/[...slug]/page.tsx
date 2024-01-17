import { getCandidateTable } from "../fetch";
import { CostTable } from "./cost-table";

export default async function Page({
    params,
    searchParams,
}: {
    params: { slug: string[] };
    searchParams: { [key: string]: string | undefined };
}) {
    const searchType = params.slug[0];
    const brand = params.slug[1];
    const candidateTableData = await getCandidateTable(searchType, brand);

    return <CostTable costTableDataSet={candidateTableData.data} />;
}
