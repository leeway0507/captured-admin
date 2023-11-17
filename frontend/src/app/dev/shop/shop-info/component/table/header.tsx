"use client";

import { shopInfoProps } from "../../../type";
import { createColumnHelper } from "@tanstack/react-table";
import { TableCell } from "@/app/components/default-table/default-header-function";
import { toast } from "react-toastify";
import { createShopInfo } from "../fetch";

type Option = {
    label: string;
    value: string;
};

const columnHelper = createColumnHelper<shopInfoProps>();

const boolArray = () => {
    return [
        { value: true, label: "true" },
        { value: false, label: "false" },
    ];
};

export const updateToDB = (props: any) => {
    const rowData = props.row.original;

    const handler = async () => {
        console.log("rowData");
        console.log(rowData);
        await createShopInfo(rowData).then((res) => {
            res.status === 200 ? toast.success("업데이트 성공") : toast.error("업데이트 실패");
        });
    };
    return (
        <button onClick={handler} className="bg-main-black text-white p-2 active:bg-blue-black whitespace-nowrap">
            DB 저장
        </button>
    );
};

export const productCardColumns = [
    columnHelper.display({
        header: "기능",
        cell: updateToDB,
    }),
    columnHelper.accessor("shopName", {
        header: "스토어 이름",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("country", {
        header: "국가",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("shopUrl", {
        header: "주소",
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
];
