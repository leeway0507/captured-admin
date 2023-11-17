"use client";

import { productCardColumns } from "./header";
import { CreateproductCardProps } from "@/app/types/type";
import { BasicTable, TableData } from "@/app/components/default-table/default-table";
import ProductInfoPagination from "./product-info-pagination";
import { useEffect, useState } from "react";
import { getProduct } from "../fetch";

export interface pageDataProps {
    data: CreateproductCardProps[];
    currentPage: number;
    lastPage: number;
}

export const ProductInfoTable = () => {
    const [newPageData, setNewPageData] = useState<pageDataProps>({
        data: [],
        currentPage: 0,
        lastPage: 0,
    });

    useEffect(() => {
        getProduct(1).then((res) => {
            setNewPageData(res.data);
        });
    }, []);

    const { data, currentPage, lastPage } = newPageData;
    // @ts-ignore
    const table = TableData({ data: newPageData.data, columns: productCardColumns });

    return (
        <div>
            <div className="sticky top-0 bg-white w-full z-10">
                <ProductInfoPagination currentPage={currentPage} lastPage={lastPage} setPageData={setNewPageData} />
            </div>
            <BasicTable table={table} />
            <div className="pt-4 pb-8">
                <ProductInfoPagination currentPage={currentPage} lastPage={lastPage} setPageData={setNewPageData} />
            </div>
        </div>
    );
};
