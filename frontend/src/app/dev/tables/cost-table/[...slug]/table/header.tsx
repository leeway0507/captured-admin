"use client";
import Image from "next/image";
import Link from "next/link";

import { productCardProps } from "./table";
import { createColumnHelper } from "@tanstack/react-table";
import { ChangeEvent, MouseEvent, useState, useEffect } from "react";
import { updateCandidate } from "../../../candidate-table/[...slug]/fetch";
import { toast } from "react-toastify";

const candidateClass = "p-2 h-[200px] flex-center";

type Option = {
    label: string;
    value: string;
};

const columnHelper = createColumnHelper<productCardProps>();

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

const handleCandidate = (event: any) => {
    const { id, status } = event.target.dataset;

    const reverseStatus = status === "1" ? 2 : 1;

    updateCandidate(id, reverseStatus).then((res) => {
        if (res.status === 200) {
            event.target.className =
                reverseStatus === 2 ? `bg-green-200 ${candidateClass}` : `bg-yellow-200 ${candidateClass}`;
            event.target.dataset.status = reverseStatus;
            toast.success("업데이트 성공", { position: "top-left", autoClose: 1000 });
        }
    });
};

export const productCardColumns = [
    columnHelper.accessor("candidate", {
        header: "추적여부",
        cell: (props) => (
            <div
                className={`${props.getValue() === 2 ? "bg-green-200" : "bg-yellow-200"} ${candidateClass}`}
                data-id={props.row.original.shopProductCardId}
                data-status={props.getValue()}
                onClick={handleCandidate}>
                {props.getValue() === 2 ? "수집 제품" : "후보 제품"}
            </div>
        ),
    }),
    columnHelper.accessor("shopProductImgUrl", {
        header: "이미지",
        cell: (props) => (
            <div>
                <div className="relative h-[200px] w-[200px] ">
                    <Image
                        src={props.getValue()}
                        alt={props.row.original.shopProductName}
                        fill
                        style={{ objectFit: "contain" }}
                    />
                </div>
            </div>
        ),
    }),

    columnHelper.accessor("productId", {
        header: "상품 ID",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),

    columnHelper.accessor("shopName", {
        header: "스토어명",
    }),
    columnHelper.accessor("shopProductName", {
        header: "상품명",
        cell: (props) => (
            <div className="max-w-[200px] overflow-hidden">
                <Link
                    href={props.row.original.productUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="underline text-blue-700 pointer-cursor">
                    <div>{props.getValue()}</div>
                </Link>
            </div>
        ),
    }),

    columnHelper.accessor("brandName", {
        header: "브랜드명",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),

    columnHelper.accessor("korPrice", {
        header: "한국 가격",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("usPrice", {
        header: "미국 가격",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("originalPriceCurrency", {
        header: "통화",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("originalPrice", {
        header: "원래 가격",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("soldOut", {
        header: "품절여부",
        cell: TableCell,
        meta: {
            type: "select",
            options: boolArray(),
        },
    }),
    columnHelper.accessor("updatedAt", {
        header: "업데이트 날짜",
    }),

    columnHelper.display({
        id: "edit",
        cell: EditCell,
    }),
];
