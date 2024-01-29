import { getCandidateTable } from "../fetch";
import { CostTable } from "./cost-table";

import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "후보 테이블",
    description: "...",
};

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
