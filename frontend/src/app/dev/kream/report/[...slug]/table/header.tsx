import { createColumnHelper } from "@tanstack/react-table";
import { scrapResultProps } from "./scrap-result-table";
import Link from "next/link";

const columnHelper = createColumnHelper<scrapResultProps>();

export const columns = [
    columnHelper.accessor("kreamId", {
        header: "kream Id",
        cell: (row) => {
            const value = row.getValue();
            return (
                <Link target="_blank" href={`http://kream.co.kr/products/${value}`} className="underline text-blue-600">
                    {value}
                </Link>
            );
        },
    }),
    columnHelper.accessor("productCard", {
        cell: (row) => {
            const value = row.getValue();
            return (
                <div className={` ${value.includes("success") ? "bg-green-500" : "bg-rose-500"} text-white`}>
                    {value}
                </div>
            );
        },
    }),
    columnHelper.accessor("tradingVolume", {
        header: "Trading Volume",
        cell: (row) => {
            const value = row.getValue();
            return (
                <div className={` ${value.includes("success") ? "bg-green-500" : "bg-rose-500"} text-white`}>
                    {value}
                </div>
            );
        },
    }),
    columnHelper.accessor("buyAndSell", {
        header: "buy And Sell",
        cell: (row) => {
            const value = row.getValue();
            return (
                <div className={` ${value.includes("success") ? "bg-green-500" : "bg-rose-500"} text-white`}>
                    {value}
                </div>
            );
        },
    }),
];
