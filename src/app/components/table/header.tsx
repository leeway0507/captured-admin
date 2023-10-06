"use client";

import { CreateproductCardProps } from "@/app/types/type";
import { createColumnHelper } from "@tanstack/react-table";
import { ChangeEvent, MouseEvent, useState, useEffect } from "react";

type Option = {
    label: string;
    value: string;
};

const columnHelper = createColumnHelper<CreateproductCardProps>();

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
        if (elName === "done") {
            meta?.updateData(row.index, "edit");
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

const imgArray = () => {
    if (process.env.NEXT_PUBLIC_IMAGE_TYPE === undefined) return null;

    return JSON.parse(process.env.NEXT_PUBLIC_IMAGE_TYPE).map((v: string) => {
        return { label: v, value: v };
    });
};
const brandArray = () => {
    if (process.env.NEXT_PUBLIC_BRAND === undefined) return null;

    return JSON.parse(process.env.NEXT_PUBLIC_BRAND).map((v: string) => {
        return { label: v, value: v };
    });
};
const categoryArray = () => {
    if (process.env.NEXT_PUBLIC_CATEGORY === undefined) return null;

    return JSON.parse(process.env.NEXT_PUBLIC_CATEGORY).map((v: string) => {
        return { label: v, value: v };
    });
};

export const productCardColumns = [
    columnHelper.accessor("brand", {
        header: "Brand",
        cell: TableCell,
        meta: {
            type: "select",
            options: brandArray(),
        },
    }),
    columnHelper.accessor("productName", {
        header: "Product Name",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("productId", {
        header: "Product ID",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("price", {
        header: "Price",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("shippingFee", {
        header: "Shipping Fee",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("intl", {
        header: "Intl",
        cell: TableCell,
        meta: {
            type: "select",
            options: [
                { value: true, label: "true" },
                { value: false, label: "false" },
            ],
        },
    }),
    columnHelper.accessor("imgType", {
        header: "Img Type",
        cell: TableCell,
        meta: {
            type: "select",
            options: imgArray(),
        },
    }),
    columnHelper.accessor("size", {
        header: "Size",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("color", {
        header: "Color",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("category", {
        header: "Category",
        cell: TableCell,
        meta: {
            type: "select",
            options: categoryArray(),
        },
    }),

    columnHelper.display({
        id: "edit",
        cell: EditCell,
    }),
];
