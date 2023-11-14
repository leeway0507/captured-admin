"use client";

import { useState, useEffect } from "react";
import "./table.css";
import { flexRender, getCoreRowModel, useReactTable, getPaginationRowModel } from "@tanstack/react-table";
import { kreamTableRawDataProps } from "./type";
import { CostTableColumn } from "./header";
import Pagination from "./pagination";

export const KreamTable = ({ tableData }: { tableData: kreamTableRawDataProps[] }) => {
    const [data, setData] = useState(() => [...tableData]);

    const table = useReactTable({
        data,
        columns: CostTableColumn,
        getCoreRowModel: getCoreRowModel(),
        getPaginationRowModel: getPaginationRowModel(),
        initialState: {
            pagination: {
                pageSize: 50,
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
                                <td className="text-sm py-1" key={cell.id}>
                                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="py-5">
                <Pagination table={table} />
            </div>
        </>
    );
};
