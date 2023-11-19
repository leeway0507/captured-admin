"use client";
import Image from "next/image";
import Link from "next/link";

import { costTableDataProps } from "./cost-table";
import { createColumnHelper } from "@tanstack/react-table";
import { TableCell, OpenKreamDetail } from "@/app/components/default-table/default-header-function";
import {
    GetPrices,
    handleCandidate,
    handleRemoveCandidate,
    candidateClass,
    updateToDB,
    SendDraft,
    GetSizeTable,
} from "./cost-table-header-functions";

const columnHelper = createColumnHelper<costTableDataProps>();

const roundUpTwo = (num: number) => {
    return Math.round(num * 100) / 100;
};

const features = (props: any) => {
    const { totalPriceBeforeCardFee, cardFee } = GetPrices(props);
    const cost = Math.round(totalPriceBeforeCardFee * 1.05 + cardFee);
    return (
        <div className="flex flex-col h-[200px] justify-evenly">
            {OpenKreamDetail("productId", props.row.original.productId, cost)}
            {GetSizeTable(props)}
            {updateToDB(props)}
            {SendDraft(props)}
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
                    className={`${
                        props.getValue() === 2 ? "bg-green-200" : "bg-yellow-200"
                    } ${candidateClass} flex-col`}
                    data-id={props.row.original.shopProductCardId}
                    data-status={props.getValue()}
                    onClick={handleCandidate}>
                    <div>사이즈</div>
                    <div>{props.getValue() === 2 ? "수집중" : "미수집"}</div>
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
        sortDescFirst: true,
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
        cell: TableCell,
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
    columnHelper.display({
        header: "실판매가",
        cell: (props) => {
            const productInfo = props.row.original.productInfo;
            const value = productInfo ? (productInfo.price + productInfo.shippingFee).toLocaleString() : "미판매 상품";
            const sellingPrice = productInfo ? productInfo.price.toLocaleString() : "-";
            const shippingFee = productInfo ? productInfo.shippingFee.toLocaleString() : "-";
            return (
                <div className="flex-center flex-col">
                    <div className="font-bold text-rose-500">{value}</div>
                    <div className="font-bold text-rose-300">({sellingPrice})</div>
                    <div className="font-bold text-rose-200">({shippingFee})</div>
                </div>
            );
        },
    }),
    columnHelper.display({
        header: "예상이익",
        cell: (props) => {
            const productInfo = props.row.original.productInfo;
            const { totalPriceBeforeCardFee, cardFee } = GetPrices(props);
            const cost = Math.round(totalPriceBeforeCardFee + cardFee);
            const value = productInfo ? (productInfo.price + productInfo.shippingFee - cost).toLocaleString() : "-";

            return <div className="text-green-700">{value}</div>;
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
            const intlShipPrice = props.row.original.shopInfo.intlShipPrice;
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
