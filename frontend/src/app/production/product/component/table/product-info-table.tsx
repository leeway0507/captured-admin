"use client";

import { productCardColumns } from "./header";
import { CreateproductCardProps } from "@/app/types/type";
import DefaultTable from "@/app/components/default-table/default-table";

export const ProductInfoTable = ({ tableData }: { tableData: CreateproductCardProps[] }) => {
    // @ts-ignore
    return <DefaultTable data={tableData} columns={productCardColumns} />;
};
