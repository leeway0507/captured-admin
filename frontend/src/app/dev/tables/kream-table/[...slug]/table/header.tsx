"use client";
import Image from "next/image";
import Link from "next/link";

import { kreamTableRawDataProps } from "./type";
import { createColumnHelper } from "@tanstack/react-table";
import KreamProductModal from "../modal/kream-product-modal";
import { useState } from "react";

// const handleCandidate = (event: any) => {
//     const { id, status } = event.target.dataset;

//     const reverseStatus = status === "true" ? false : true;

//     console.log(event.target, id, reverseStatus);

//     updateCandidate(id, reverseStatus).then((res) => {
//         if (res.status === 200) {
//             event.target.className = reverseStatus ? "bg-green-400 p-2" : "bg-rose-300 p-2";
//             event.target.dataset.status = reverseStatus;
//             toast.success("업데이트 성공", { position: "top-left", autoClose: 1000 });
//         }
//     });
// };

const OpenDetail = (props: any) => {
    const { kreamId } = props.row.original;
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
            <button
                className="bg-gray-200 hover:bg-gray-300 p-2"
                onClick={() => {
                    setIsOpen(true);
                }}>
                상세정보
            </button>
            {isOpen && (
                <KreamProductModal
                    searchType="kreamId"
                    value={kreamId}
                    isOpen={isOpen}
                    setIsOpen={setIsOpen}
                    cost={9000000}
                />
            )}
        </>
    );
};

const columnHelper = createColumnHelper<kreamTableRawDataProps>();

export const CostTableColumn = [
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
    columnHelper.display({
        header: "상세정보",
        cell: OpenDetail,
    }),
];
