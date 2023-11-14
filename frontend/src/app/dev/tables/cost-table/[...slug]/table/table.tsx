"use client";

import { useState, useEffect, ChangeEvent, MouseEvent } from "react";
import { productCardColumns } from "./header";
import "./table.css";
import { flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import Pagination from "./pagination";

export interface productCardProps {
    shopProductCardId: number;
    shopProductName: string;
    shopProductImgUrl: string;
    productUrl: string;
    shopName: string;
    brandName: string;
    productId: string;
    korPrice: number;
    usPrice: number;
    originalPriceCurrency: string;
    originalPrice: number;
    soldOut: boolean;
    candidate: number;
    updatedAt: Date;
}

export const CostTable = ({ defaultData }: { defaultData: productCardProps[] }) => {
    useEffect(() => {
        setData(defaultData);
        setOriginalData(defaultData);
    }, [defaultData]);

    const columns = productCardColumns;
    const [data, setData] = useState(defaultData);
    const [originalData, setOriginalData] = useState(defaultData);
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
        <>
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
                                <td className="text-xs" key={cell.id}>
                                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </>
    );
};
