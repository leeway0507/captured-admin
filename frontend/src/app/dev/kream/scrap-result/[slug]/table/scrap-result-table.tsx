import { getCoreRowModel, useReactTable } from "@tanstack/react-table";
import DefaultTable from "@/app/components/default-table/default-table";
import { columns } from "./header";

export interface scrapResultProps {
    kreamId: number;
    productCard: boolean;
    tradingVolume: boolean;
    bridge: boolean;
    buyAndSell: boolean;
    error: string;
}

const ScrapResultTable = ({ tableData }: { tableData: scrapResultProps[] }) => {
    // @ts-ignore
    return <DefaultTable data={tableData} columns={columns} />;
};

export default ScrapResultTable;
