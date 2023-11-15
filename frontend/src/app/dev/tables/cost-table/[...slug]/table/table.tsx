"use client";

import { useState } from "react";
import { productCardColumns } from "./header";
import "./table.css";
import { flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import Pagination from "./pagination";
import { shopInfoProps } from "@/app/dev/shop/type";
import { productCardProps } from "../../../candidate-table/[...slug]/main";

export interface costTableDataProps extends productCardProps, shopInfoProps {
    errorRate: number;
    cardRate: number;
    VATRate: number;
    customRate: number;
    currency: number;
    buyingCurrency: number;
    usCurrency: number;
    sellingPrice: number;
    productInfo: productInfoProps;
}

interface costTableDataSetProps {
    shopInfos: shopInfoProps[];
    dbData: productCardProps[];
    currency: { data: { [key: string]: any }; updatedAt: Date };
}

interface productInfoProps {
    sku: number;
    productId: string;
    shippingFee: number;
    price: number;
}

const createTableData = (costTableDataSet: costTableDataSetProps, productInfo: productInfoProps[]) => {
    const { shopInfos, dbData, currency } = costTableDataSet;
    const buyingCurrency = currency.data;
    return dbData.map((row) => {
        const shopInfo = shopInfos.find((shopInfo) => shopInfo.shopName === row.shopName);
        const product = productInfo.find((productInfo) => productInfo.productId === row.productId);

        return {
            ...row,
            ...shopInfo,
            errorRate: 1.025,
            cardRate: 0.03,
            VATRate: 0.1,
            customRate: 0.13,
            buyingCurrency: buyingCurrency[row.originalPriceCurrency],
            usCurrency: buyingCurrency["USD"],
            sellingPrice: 0,
            productInfo: product,
        };
    });
};

export const CostTable = ({
    costTableDataSet,
    productInfo,
}: {
    costTableDataSet: costTableDataSetProps;
    productInfo: productInfoProps[];
}) => {
    //prettier-ignore
    const tableData: costTableDataProps[] = createTableData(costTableDataSet,productInfo);

    const columns = productCardColumns;
    const [data, setData] = useState(tableData);
    const [originalData, setOriginalData] = useState(tableData);

    const [editedRows, setEditedRows] = useState({});
    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
        meta: {
            editedRows,
            setEditedRows,
            revertData: (rowIndex: number, revert: boolean) => {
                if (revert) {
                    setData((old) => old.map((row, index) => (index === rowIndex ? originalData[rowIndex] : row)));
                } else {
                    setOriginalData((old) => old.map((row, index) => (index === rowIndex ? data[rowIndex] : row)));
                    // api.createShopInfo(data[rowIndex]);
                }
            },
            updateData: (rowIndex: number, columnId: string, value: string) => {
                setData((old) =>
                    old.map((row, index) => {
                        if (index === rowIndex) {
                            return {
                                ...old[rowIndex],
                                [columnId]: value,
                            };
                        }
                        return row;
                    })
                );
            },
        },
    });
    return (
        <div className="flex flex-col w-full">
            <div className="sticky top-0 bg-white w-full z-10">
                <Pagination table={table} />
            </div>
            <table>
                <thead>
                    {table.getHeaderGroups().map((headerGroup) => (
                        <tr key={headerGroup.id}>
                            {headerGroup.headers.map((header) => (
                                <th
                                    key={header.id}
                                    className="text-sm py-2 px-4 sticky top-8 whitespace-nowrap bg-blue-100 z-10">
                                    {header.isPlaceholder
                                        ? null
                                        : flexRender(header.column.columnDef.header, header.getContext())}
                                </th>
                            ))}
                        </tr>
                    ))}
                </thead>
                <tbody>
                    {table.getRowModel().rows.map((row) => (
                        <tr key={row.id}>
                            {row.getVisibleCells().map((cell) => (
                                <td className="text-xs px-2 min-w-[100px]" key={cell.id}>
                                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};
