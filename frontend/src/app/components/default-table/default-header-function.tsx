"use client";
import { useState } from "react";
import Select from "react-select";
import KreamProductModal from "@/app/dev/tables/kream-table/[...slug]/modal/kream-product-modal";

export const TableCell = (props: any) => {
    const { row, column, table, getValue } = props;
    const initialValue = getValue();
    const [value, setValue] = useState(typeof initialValue === "boolean" ? initialValue.toString() : initialValue);
    const columnMeta = column.columnDef.meta;
    const tableMeta = table.options.meta;

    const onBlur = () => {
        tableMeta?.updateData(row.index, column.id, value);
    };
    const onSelectChange = (e: any) => {
        setValue(e.value);
        tableMeta?.updateData(row.index, column.id, e.value);
    };

    return columnMeta?.type === "select" ? (
        <Select
            defaultValue={columnMeta?.options.find((v: any) => v.value === initialValue)}
            options={columnMeta?.options}
            onChange={onSelectChange}
            className="min-w-[100px] max-w-full"
        />
    ) : (
        <input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onBlur={onBlur}
            type={columnMeta?.type || "text"}
            className="bg-transparent border-transparent border-b-sub-black focus:outline-none rounded-none text-center w-[150px] max-w-full"
        />
    );
};

export const OpenKreamDetail = (searchType: string, value: string, cost: number) => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
            <button
                className="bg-gray-200 hover:bg-gray-300 p-2 whitespace-nowrap"
                onClick={() => {
                    setIsOpen(true);
                }}>
                크림정보
            </button>
            {isOpen && (
                <KreamProductModal
                    searchType={searchType}
                    value={value}
                    isOpen={isOpen}
                    setIsOpen={setIsOpen}
                    cost={Math.round(cost)}
                />
            )}
        </>
    );
};
