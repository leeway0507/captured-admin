"use client";

import { useState } from "react";
import { column } from "./header";
import "./table.css";
import { flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import { orderHistoryProps } from "@/app/types/type";

export const Table = ({ defaultData }: { defaultData: orderHistoryProps[] }) => {
    const columns = column;
    const [data, setData] = useState(() => [...defaultData]);
    const [originalData, setOriginalData] = useState(() => [...defaultData]);
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
            <table className="w-full">
                <thead>
                    {table.getHeaderGroups().map((headerGroup) => (
                        <tr key={headerGroup.id}>
                            {headerGroup.headers.map((header) => (
                                <th key={header.id} className="text-sm">
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
