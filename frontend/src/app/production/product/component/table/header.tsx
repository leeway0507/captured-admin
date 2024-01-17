"use client";

import Image from "next/image";

import { CreateproductCardProps } from "@/app/types/type";
import { createColumnHelper } from "@tanstack/react-table";
import { TableCell, OpenKreamDetail } from "@/app/components/default-table/default-header-function";
import { toast } from "react-toastify";
import { GetSizeTable } from "@/app/dev/tables/candidate/[...slug]/cost-table-header-functions";

import * as func from "./header-function";

const columnHelper = createColumnHelper<CreateproductCardProps>();

const extraFetures = (props: any) => {
    return (
        <div className="flex flex-col h-[200px] justify-evenly">
            {OpenKreamDetail("productId", props.row.original.productId, 0, false)}
            {GetSizeTable(props)}
        </div>
    );
};
const features = (props: any) => {
    return (
        <div className="flex flex-col h-[200px] justify-evenly">
            {func.handleUpdateProduct(props)}
            {func.UploadImage(props)}
            {func.handleDeleteProduct(props)}
        </div>
    );
};

export const productCardColumns = [
    columnHelper.accessor("deploy", {
        header: "전시/미전시",
        cell: (props) => {
            const { sku, deploy } = props.row.original;
            if (sku === undefined) {
                return toast.error("sku가 없습니다.");
            }
            return (
                <button
                    onClick={(e) => func.handleCandidate(e, sku, deploy!)}
                    className={`${
                        deploy === 0 ? "bg-rose-300" : "bg-green-300"
                    } h-[180px] w-[80px] text-sm flex-center flex-col`}
                    data-sku={sku}
                    data-deploy={deploy}>
                    <div>{deploy === 0 ? "미전시" : "전시중"}</div>
                    <div>sku : {sku}</div>
                </button>
            );
        },

        filterFn: (row, columnId, value, addMeta) => {
            switch (value.label) {
                case "전체":
                    return true;
                case "전시":
                    return row.original.deploy === 1;
                case "미전시":
                    return row.original.deploy === 0;
                default:
                    return true;
            }
        },
        meta: {
            type: "select",
            options: [
                { value: "전체", label: "전체" },
                { value: "미전시", label: "미전시" },
                { value: "전시", label: "전시" },
            ],
        },
    }),
    columnHelper.accessor("sku", {
        header: "SKU",
        cell: (props) => {
            const sku = props.getValue();
            const productImgUrl = `${process.env.NEXT_PUBLIC_MOBILE_IMAGE_URL}/product/${sku}/thumbnail.webp`;
            return (
                <div className="relative h-[180px] w-[180px] ">
                    <Image
                        id={sku!.toString()}
                        src={productImgUrl}
                        alt={props.row.original.productName}
                        fill
                        sizes="150px"
                        style={{ objectFit: "contain" }}
                    />
                </div>
            );
        },
        filterFn: (row, columnId, value, addMeta) => {
            return row.original.sku === Number(value);
        },
        meta: {
            type: "text",
        },
    }),
    columnHelper.display({
        header: "기능",
        cell: features,
    }),
    columnHelper.display({
        header: "기타기능",
        cell: extraFetures,
    }),
    columnHelper.accessor("brand", {
        header: "브랜드",
        cell: func.BrandNameCell,
    }),
    columnHelper.accessor("productName", {
        header: "제품명",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("korProductName", {
        header: "제품명(한)",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("productId", {
        header: "제품 아이디",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("price", {
        header: "판매가",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("shippingFee", {
        header: "배송비",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("intl", {
        header: "배송",
        cell: TableCell,
        meta: {
            type: "select",
            options: [
                { value: true, label: "해외" },
                { value: false, label: "국내" },
            ],
        },
    }),
    columnHelper.accessor("imgType", {
        header: "이미지 타입",
        cell: TableCell,
        meta: {
            type: "select",
            options: func.imgArray(),
        },
    }),
    columnHelper.accessor("color", {
        header: "색상",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("category", {
        header: "카테고리",
        cell: TableCell,
        meta: {
            type: "select",
            options: func.categoryArray(),
        },
    }),
    columnHelper.accessor("categorySpec", {
        header: "카테고리 상세",
        cell: func.CategorySpecCell,
    }),
    columnHelper.accessor("searchInfo", {
        header: "검색어",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
];
