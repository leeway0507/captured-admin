"use client";
import Image from "next/image";
import Link from "next/link";

import { costTableRawDataProps } from "./type";
import { createColumnHelper } from "@tanstack/react-table";
import { toast } from "react-toastify";

import { updateCandidate } from "../fetch";
import { useState } from "react";
import KreamProductModal from "../../../kream-table/[...slug]/modal/kream-product-modal";

const OpenDetail = (props: any) => {
    const { productId, totalPriceBeforeCardFee } = props.row.original;
    const [isOpen, setIsOpen] = useState(false);

    const cost = totalPriceBeforeCardFee * 1.05 + 3000;

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
                    searchType="productId"
                    value={productId}
                    isOpen={isOpen}
                    setIsOpen={setIsOpen}
                    cost={Math.round(cost)}
                />
            )}
        </>
    );
};

const handleCandidate = (event: any) => {
    const { id, status } = event.target.dataset;

    const reverseStatus = status === "true" ? false : true;

    console.log(event.target, id, reverseStatus);

    updateCandidate(id, reverseStatus).then((res) => {
        if (res.status === 200) {
            event.target.className = reverseStatus ? "bg-green-400 p-2" : "bg-rose-300 p-2";
            event.target.dataset.status = reverseStatus;
            toast.success("업데이트 성공", { position: "top-left", autoClose: 1000 });
        }
    });
};

const columnHelper = createColumnHelper<costTableRawDataProps>();

export const CostTableColumn = [
    columnHelper.accessor("candidate", {
        header: "추적여부",
        cell: (props) => (
            <div
                className={`${props.getValue() ? "bg-green-400" : "bg-rose-300"} p-2 `}
                data-id={props.row.original.shopProductCardId}
                data-status={props.getValue()}
                onClick={handleCandidate}>
                {props.row.original.productId}
            </div>
        ),
    }),

    columnHelper.accessor("shopProductName", {
        header: "이미지",
        cell: (props) => (
            <div>
                <div className="relative h-[200px] w-[200px] ">
                    <Image
                        src={props.row.original.shopProductImgUrl}
                        alt={props.getValue()}
                        fill
                        style={{ objectFit: "contain" }}
                    />
                </div>
            </div>
        ),
    }),
    columnHelper.display({
        header: "크림상세정보",
        cell: OpenDetail,
    }),
    columnHelper.accessor("originalPrice", {
        header: "구매가(외화)",
        cell: (props) => (
            <div className="flex-center flex-col">
                <div className="text-xs">{props.row.original.originalPriceCurrency}</div>
                <div
                    className="text-xs text-blue-500 line-through
">
                    ({props.getValue()})
                </div>
                <div>{props.row.original.taxReductionOriginalPrice}</div>

                <div>$ {props.row.original.usPrice}</div>
            </div>
        ),
    }),
    columnHelper.accessor("sellPrice10P", {
        header: "마진 범위",
        cell: (props) => {
            const sell10P = props.getValue() - props.row.original.totalPrice;
            const sell20P = props.row.original.sellPrice20P - props.row.original.totalPrice;
            return (
                <div className="flex flex-col gap-4">
                    <div className="flex-center flex-col gap-1">
                        <div className="text-green-700 text-bold">{props.getValue().toLocaleString()}</div>
                        <div className="text-green-700 text-bold underline">(+ {sell10P.toLocaleString()})</div>
                    </div>
                    <div className="flex-center flex-col gap-1">
                        <div className="text-green-500 text-bold">
                            {props.row.original.sellPrice20P.toLocaleString()}
                        </div>
                        <div className="text-green-500 text-bold underline">(+ {sell20P.toLocaleString()})</div>
                    </div>
                </div>
            );
        },
    }),

    columnHelper.accessor("totalPrice", {
        header: "총 구매가",
        cell: (props) => {
            return (
                <div>
                    <div>{props.getValue().toLocaleString()}</div>
                </div>
            );
        },
    }),
    columnHelper.accessor("korPrice", {
        header: "구매가",
        cell: (props) => <div>{props.getValue().toLocaleString()}</div>,
    }),
    columnHelper.accessor("intlShipKorPrice", {
        header: "해외배송비",
        cell: (props) => (
            <div>
                <div>{props.getValue().toLocaleString()}</div>
                <div className="text-blue-500 text-xs">({props.row.original.intlShipPrice})</div>
            </div>
        ),
    }),
    columnHelper.accessor("customFee", {
        header: "관세",
        cell: (props) => <div>{props.getValue().toLocaleString()}</div>,
    }),
    columnHelper.accessor("VATFee", {
        header: "부가세",
        cell: (props) => <div>{props.getValue().toLocaleString()}</div>,
    }),
    columnHelper.accessor("cardFee", {
        header: "카드수수료",
        cell: (props) => <div>{props.getValue().toLocaleString()}</div>,
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
];
