"use client";

import { orderHistoryProps } from "@/app/types/type";
import { createColumnHelper } from "@tanstack/react-table";

const columnHelper = createColumnHelper<orderHistoryProps>();

export const column = [
    columnHelper.accessor("orderedAt", {
        header: "주문일",
    }),
    columnHelper.accessor("orderId", {
        header: "주문 ID",
    }),
    columnHelper.accessor("userId", {
        header: "고객번호",
    }),
    columnHelper.accessor("userOrderNumber", {
        header: "주문횟수",
    }),
    columnHelper.accessor("addressId", {
        header: "주소",
    }),
    columnHelper.accessor("orderTotalPrice", {
        header: "결제금액",
    }),
    columnHelper.accessor("paymentMethod", {
        header: "결제방법",
    }),
    columnHelper.accessor("paymentStatus", {
        header: "결제현황",
    }),
    columnHelper.accessor("orderStatus", {
        header: "배송현황",
    }),
];
