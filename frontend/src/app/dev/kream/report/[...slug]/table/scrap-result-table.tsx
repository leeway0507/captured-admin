import { getCoreRowModel, useReactTable } from "@tanstack/react-table";
import DefaultTable from "@/app/components/default-table/default-table";
import { columns } from "./header";

export interface scrapResultProps {
    kreamId: string;
    productCard: string;
    tradingVolume: string;
    buyAndSell: string;
}

const ScrapResultTable = ({ tableData }: { tableData: scrapResultProps[] }) => {
    // @ts-ignore
    return <DefaultTable data={tableData} columns={columns} />;
};

export default ScrapResultTable;
