"use client";
import Image from "next/image";
import Link from "next/link";

import { kreamTableRawDataProps } from "./kream-table";
import { createColumnHelper } from "@tanstack/react-table";
import { OpenKreamDetailWithHover } from "@/app/components/default-table/default-header-function";

const columnHelper = createColumnHelper<kreamTableRawDataProps>();

export const kreamTableColumns = [
    columnHelper.accessor("kreamId", {
        header: "크림 아이디",
        cell: (props) => (
            <Link
                href={`https://kream.co.kr/products/${props.getValue()}`}
                target="_blank"
                rel="noreferrer"
                className="underline text-blue-700 pointer-cursor">
                {props.getValue()}
            </Link>
        ),
    }),
    columnHelper.accessor("productId", {
        header: "제품 아이디",
    }),
    columnHelper.accessor("kreamProductImgUrl", {
        header: "이미지",
        cell: (props) => (
            <div className="relative h-[200px] w-[200px] ">
                <Image
                    src={props.getValue()}
                    alt={props.row.original.kreamProductName}
                    fill
                    style={{ objectFit: "contain" }}
                />
            </div>
        ),
    }),

    columnHelper.accessor("brandName", {
        header: "브랜드",
    }),
    columnHelper.accessor("kreamProductName", {
        header: "제품명",
        cell: (props) => <div className="max-w-[250px]">{props.getValue()}</div>,
    }),
    columnHelper.accessor("tradingVolume", {
        header: "거래량",
    }),
    columnHelper.accessor("wish", {
        header: "찜 수",
    }),

    columnHelper.display({
        header: "상세정보",
        cell: (props) =>
            OpenKreamDetailWithHover(
                "kreamId",
                String(props.row.original.productId),
                props.row.original.retailPrice! > 0 ? props.row.original.retailPrice! : 1000000
            ),
    }),
    columnHelper.accessor("updatedAt", {
        header: "업데이트",
    }),
];
