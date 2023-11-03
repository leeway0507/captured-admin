"use client";

import { useState } from "react";
import "./table.css";
import { flexRender, getCoreRowModel, useReactTable, createColumnHelper } from "@tanstack/react-table";
import Link from "next/link";

export const CustomTable = ({ defaultData, tableClassName }: { defaultData: object[]; tableClassName: string }) => {
    const columnHelper = createColumnHelper();
    const columns = [
        columnHelper.accessor("kreamId", {
            header: "kream Id",
            cell: (row) => {
                return (
                    <Link
                        target="_blank"
                        href={`http://kream.co.kr/products/${row.getValue()}`}
                        className="underline text-blue-600">
                        {row.getValue()}
                    </Link>
                );
            },
        }),
        columnHelper.accessor("productCard", {
            cell: (row) => {
                return (
                    <div className={` ${row.getValue() ? "bg-green-500" : "bg-rose-500"} text-white`}>
                        {row.getValue() ? "O" : "X"}
                    </div>
                );
            },
        }),
        columnHelper.accessor("tradingVolume", {
            header: "Trading Volume",
            cell: (row) => {
                return (
                    <div className={` ${row.getValue() ? "bg-green-500" : "bg-rose-500"} text-white`}>
                        {row.getValue() ? "O" : "X"}
                    </div>
                );
            },
        }),
        columnHelper.accessor("bridge", {
            header: "Bridge",
            cell: (row) => {
                return (
                    <div className={` ${row.getValue() ? "bg-green-500" : "bg-rose-500"} text-white`}>
                        {row.getValue() ? "O" : "X"}
                    </div>
                );
            },
        }),
        columnHelper.accessor("buyAndSell", {
            header: "buy And Sell",
            cell: (row) => {
                return (
                    <div className={` ${row.getValue() ? "bg-green-500" : "bg-rose-500"} text-white`}>
                        {row.getValue() ? "O" : "X"}
                    </div>
                );
            },
        }),
        columnHelper.accessor("error", {
            header: "error",
            cell: (row) => {
                return <div className={"basis-[50%]"}>{row.getValue()}</div>;
            },
        }),
    ];

    const [data, setData] = useState(() => [...defaultData]);

    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
    });

    return (
        <>
            <table className={`${tableClassName}`}>
                <thead>
                    {table.getHeaderGroups().map((headerGroup) => (
                        <tr key={headerGroup.id}>
                            {headerGroup.headers.map((header) => (
                                <th key={header.id} className="text-sm px-2">
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
                                <td className="text-sm" key={cell.id}>
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
