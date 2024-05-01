"use client";

import { productCardColumns } from "./header";
import { shopInfoProps } from "../../../type";
import DefaultTable from "@/app/components/default-table/default-table";

export const ShopInfoTable = ({ tableData }: { tableData: shopInfoProps[] }) => {
    
    return <DefaultTable data={tableData} columns={productCardColumns} />;
};
