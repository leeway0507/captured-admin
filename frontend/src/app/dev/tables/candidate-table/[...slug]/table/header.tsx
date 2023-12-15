"use client";
import Image from "next/image";
import Link from "next/link";

import { candidateTableRawDataProps } from "./candidate-table";
import { createColumnHelper } from "@tanstack/react-table";
import { toast } from "react-toastify";

import { updateCandidate } from "../fetch";
import { OpenKreamDetail } from "@/app/components/default-table/default-header-function";

const candidateClass = "p-2 h-[200px] flex-center";

const handleCandidate = (event: any) => {
    const { id, status } = event.target.dataset;

    const reverseStatus = status === "0" ? 2 : 0;

    updateCandidate(id, reverseStatus).then((res) => {
        if (res.status === 200) {
            event.target.className =
                reverseStatus === 2 ? `bg-yellow-200 ${candidateClass}` : `bg-rose-200 ${candidateClass}`;
            event.target.dataset.status = reverseStatus;
            toast.success("업데이트 성공", { position: "top-left", autoClose: 1000 });
        }
    });
};

const columnHelper = createColumnHelper<candidateTableRawDataProps>();

export const CostTableColumn = [
    columnHelper.accessor("candidate", {
        header: "추적여부",
        cell: (props) => (
            <div
                className={`${props.getValue() ? "bg-yellow-200" : "bg-rose-200"} ${candidateClass}`}
                data-id={props.row.original.shopProductCardId}
                data-status={props.getValue()}
                onClick={handleCandidate}>
                {props.row.original.productId}
            </div>
        ),
    }),

    columnHelper.accessor("shopProductImgUrl", {
        header: "이미지(링크)",
        cell: (props) => (
            <div className="flex-center flex-col">
                <Link
                    href={props.row.original.productUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="underline text-blue-700 pointer-cursor hover:opacity-80">
                    <div className="relative h-[150px] w-[150px] ">
                        <Image
                            src={props.getValue()}
                            alt={props.row.original.shopProductName}
                            fill
                            sizes="150px"
                            style={{ objectFit: "contain" }}
                        />
                    </div>
                </Link>
                <div>{props.row.original.brandName}</div>
            </div>
        ),
    }),
    columnHelper.display({
        header: "크림상세정보",
        cell: (props) => {
            const cost = props.row.original.totalPriceBeforeCardFee * 1.05;
            return <div>{OpenKreamDetail("productId", props.row.original.productId, cost)}</div>;
        },
    }),

    columnHelper.accessor("originalPrice", {
        header: "구매가(외화)",
        cell: (props) => (
            <div className="flex-center flex-col">
                <div className="text-xs">{props.row.original.originalPriceCurrency}</div>
                <div className="text-xs text-blue-500 line-through">({props.getValue()})</div>
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
];
