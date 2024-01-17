"use client";

import { getCoreRowModel, useReactTable, getPaginationRowModel } from "@tanstack/react-table";
import DefaultTable from "@/app/components/default-table/default-table";
import { kreamTableColumns } from "./header";

export interface kreamTableRawDataProps {
    kreamId: number;
    productId: number;
    brandName: string;
    kreamProductName: string;
    kreamProductImgUrl: string;
    retailPrice?: number;
    productRelease_date?: Date;
    tradingVolume?: number;
    wish: number;
    review: number;
    updated_at: Date;
}

export const KreamTable = ({ tableData }: { tableData: kreamTableRawDataProps[] }) => {
    // @ts-ignore
    return <DefaultTable data={tableData} columns={kreamTableColumns} />;
};
