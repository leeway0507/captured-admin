"use client";

import { shopInfoProps } from "../../../type";
import { createColumnHelper } from "@tanstack/react-table";
import { ChangeEvent, MouseEvent, useState, useEffect } from "react";

type Option = {
    label: string;
    value: string;
};

const columnHelper = createColumnHelper<shopInfoProps>();

const EditCell = ({ row, table }) => {
    const meta = table.options.meta;
    const setEditedRows = (e: MouseEvent<HTMLButtonElement>) => {
        const elName = e.currentTarget.name;
        meta?.setEditedRows((old: []) => ({
            ...old,
            [row.id]: !old[row.id],
        }));
        if (elName !== "edit") {
            meta?.revertData(row.index, e.currentTarget.name === "cancel");
        }
    };
    return (
        <div className="edit-cell-container w-[50px] flex-center">
            {meta?.editedRows[row.id] ? (
                <div className="edit-cell">
                    <button onClick={setEditedRows} name="cancel">
                        X
                    </button>
                    <button onClick={setEditedRows} name="done">
                        ✔
                    </button>
                </div>
            ) : (
                <button onClick={setEditedRows} name="edit">
                    ✐
                </button>
            )}
        </div>
    );
};

const TableCell = ({ getValue, row, column, table }) => {
    const initialValue = getValue();
    const [value, setValue] = useState(typeof initialValue === "boolean" ? initialValue.toString() : initialValue);
    const columnMeta = column.columnDef.meta;
    const tableMeta = table.options.meta;

    const onBlur = () => {
        tableMeta?.updateData(row.index, column.id, value);
    };
    const onSelectChange = (e: ChangeEvent<HTMLSelectElement>) => {
        setValue(e.target.value);
        tableMeta?.updateData(row.index, column.id, e.target.value);
    };
    if (tableMeta?.editedRows[row.id]) {
        return columnMeta?.type === "select" ? (
            <select onChange={onSelectChange} value={initialValue}>
                {columnMeta?.options?.map((option: Option) => (
                    <option key={option.value} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select>
        ) : (
            <input
                value={value}
                onChange={(e) => setValue(e.target.value)}
                onBlur={onBlur}
                type={columnMeta?.type || "text"}
                className="max-w-[100px]"
            />
        );
    }
    return <span>{value}</span>;
};

const boolArray = () => {
    return [
        { value: true, label: "true" },
        { value: false, label: "false" },
    ];
};

export const productCardColumns = [
    columnHelper.accessor("shopName", {
        header: "스토어 이름",
    }),
    columnHelper.accessor("country", {
        header: "국가",
    }),
    columnHelper.accessor("shopUrl", {
        header: "주소",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("taxReductionRate", {
        header: "부가세.감",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("delAgcTaxReductionRate", {
        header: "배대지 부가세.감",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("domeShipPrice", {
        header: "배대지 배송비",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("intlShipPrice", {
        header: "국제배송비",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("fromUsShipping", {
        header: "미국배송",
        cell: TableCell,
        meta: {
            type: "select",
            options: boolArray(),
        },
    }),
    columnHelper.accessor("isDdp", {
        header: "DDP 여부",
        cell: TableCell,
        meta: {
            type: "select",
            options: boolArray(),
        },
    }),

    columnHelper.display({
        id: "edit",
        cell: EditCell,
    }),
];
