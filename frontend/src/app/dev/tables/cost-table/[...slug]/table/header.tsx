"use client";
import Image from "next/image";
import Link from "next/link";

import { costTableDataProps } from "./table";
import { createColumnHelper } from "@tanstack/react-table";

import {
    OpenDetail,
    TableCell,
    GetPrices,
    handleCandidate,
    handleRemoveCandidate,
    candidateClass,
    updateToDB,
    sendDraft,
} from "./header-functions";

const columnHelper = createColumnHelper<costTableDataProps>();

const boolArray = () => {
    return [
        { value: true, label: "true" },
        { value: false, label: "false" },
    ];
};

const roundUpTwo = (num: number) => {
    return Math.round(num * 100) / 100;
};

const features = (props: any) => {
    return (
        <div className="flex flex-col h-[200px] justify-evenly">
            {OpenDetail(props)}
            {updateToDB(props)}
            {sendDraft(props)}
        </div>
    );
};

export const productCardColumns = [
    columnHelper.accessor("candidate", {
        header: "추적여부",
        cell: (props) => (
            <>
                <div
                    id={`status-${props.row.original.shopProductCardId}`}
                    className={`${props.getValue() === 2 ? "bg-green-200" : "bg-yellow-200"} ${candidateClass}`}
                    data-id={props.row.original.shopProductCardId}
                    data-status={props.getValue()}
                    onClick={handleCandidate}>
                    {props.getValue() === 2 ? "수집 제품" : "후보 제품"}
                </div>
                <div
                    className={`bg-rose-200 flex-center h-[50px] mt-2`}
                    data-id={props.row.original.shopProductCardId}
                    data-status={1}
                    onClick={handleRemoveCandidate}>
                    후보 제거
                </div>
            </>
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
                <div>{props.row.original.shopName}</div>
                <div>{props.row.original.brandName}</div>
            </div>
        ),
    }),
    columnHelper.display({
        header: "기능",
        cell: features,
    }),

    columnHelper.accessor("productId", {
        header: "상품 ID",
        cell: (props) => <div className="w-[150px]">{TableCell(props)}</div>,
        meta: {
            type: "text",
        },
    }),

    columnHelper.accessor("coupon", {
        header: "쿠폰",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("sellingPrice", {
        header: "실판매가",
        cell: (props) => <div className="font-bold text-rose-500">{props.getValue()}</div>,
    }),
    columnHelper.display({
        header: "예상이익",
        cell: (props) => {
            const { sellingPrice } = props.row.original;
            const { totalPriceBeforeCardFee, cardFee } = GetPrices(props);
            const value = Math.round(totalPriceBeforeCardFee + cardFee);
            const profit = sellingPrice - value;
            return <div className="text-green-700">{profit.toLocaleString()}</div>;
        },
    }),
    columnHelper.display({
        header: "마진 범위",
        cell: (props) => {
            const { sellPrice10P, sellPrice20P, totalPriceBeforeCardFee, cardFee } = GetPrices(props);
            const sell10P = Math.round(sellPrice10P - (totalPriceBeforeCardFee + cardFee));
            const sell20P = Math.round(sellPrice20P - (totalPriceBeforeCardFee + cardFee));
            return (
                <div className="flex flex-col gap-4">
                    <div className="flex-center flex-col gap-1">
                        <div className="text-green-700 text-bold">{sellPrice10P.toLocaleString()}</div>
                        <div className="text-green-700 text-bold underline">(+ {sell10P.toLocaleString()})</div>
                    </div>
                    <div className="flex-center flex-col gap-1">
                        <div className="text-green-500 text-bold">{sellPrice20P.toLocaleString()}</div>
                        <div className="text-green-500 text-bold underline">(+ {sell20P.toLocaleString()})</div>
                    </div>
                </div>
            );
        },
    }),
    columnHelper.display({
        header: "원가",
        cell: (props) => {
            const { totalPriceBeforeCardFee, cardFee } = GetPrices(props);
            const value = Math.round(totalPriceBeforeCardFee + cardFee);
            return (
                <div>
                    <div>{value.toLocaleString()}</div>
                </div>
            );
        },
    }),

    columnHelper.display({
        header: "구매가",
        id: "koreaPrice",
        cell: (props) => {
            const { coupon, originalPrice, originalPriceCurrency } = props.row.original;

            const { korPrice, usPrice, PriceWithCoupon, taxReductionOriginalPrice } = GetPrices(props);

            return (
                <div>
                    <div className="text-deep-gray line-through ">({originalPrice})</div>
                    <div>₩ {Math.round(korPrice).toLocaleString()}</div>
                    <div className="text-blue-500 text-xs whitespace-nowrap">
                        {coupon > 0 ? (
                            <div>쿠폰가 : {roundUpTwo(PriceWithCoupon)}</div>
                        ) : (
                            <div>
                                ({originalPriceCurrency} {roundUpTwo(taxReductionOriginalPrice)})
                            </div>
                        )}
                    </div>

                    <div>$ {roundUpTwo(usPrice)}</div>
                </div>
            );
        },
    }),

    columnHelper.display({
        header: "해외배송비",
        cell: (props) => {
            const { intlShipPrice } = props.row.original;
            const { intlShipKorPrice } = GetPrices(props);

            return (
                <div>
                    <div>
                        <div>₩ {intlShipKorPrice.toLocaleString()}</div>
                        <div className="text-blue-500 text-xs">({intlShipPrice})</div>
                    </div>
                </div>
            );
        },
    }),
    columnHelper.display({
        header: "관세",
        cell: (props) => {
            const { customRate } = props.row.original;

            const { customFee } = GetPrices(props);
            return (
                <div>
                    <div>{customFee}</div>
                    <div className="text-blue-500 text-xs">({customRate})</div>
                </div>
            );
        },
    }),
    columnHelper.display({
        header: "부가세",
        cell: (props) => {
            const { VATRate } = props.row.original;
            const { VATFee } = GetPrices(props);
            return (
                <div>
                    <div>{VATFee}</div>
                    <div className="text-blue-500 text-xs">({VATRate})</div>
                </div>
            );
        },
    }),
    columnHelper.display({
        header: "카드수수료",
        cell: (props) => {
            const { cardRate } = props.row.original;
            const { cardFee } = GetPrices(props);
            return (
                <div>
                    <div>{cardFee}</div>
                    <div className="text-blue-500 text-xs">({cardRate})</div>
                </div>
            );
        },
    }),

    columnHelper.accessor("soldOut", {
        header: "품절여부",
    }),
    columnHelper.accessor("updatedAt", {
        header: "업데이트",
        cell: (props) => {
            const date = props.getValue().toString().split("T");
            return (
                <div className="flex flex-col gap-1">
                    <div>{date[0]}</div>
                    <div>{date[1]}</div>
                </div>
            );
        },
    }),
];
