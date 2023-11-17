"use client";

import { column } from "./header";
import { orderHistoryProps } from "@/app/types/type";
import DefaultTable from "@/app/components/default-table/default-table";

export const OrderHistoryTable = ({ tableData }: { tableData: orderHistoryProps[] }) => {
    // @ts-ignore
    return <DefaultTable data={tableData} columns={orderHistoryProps} />;
};
