import { createColumnHelper } from "@tanstack/react-table";
import { scrapResultProps } from "./scrap-result-table";
import Link from "next/link";

const columnHelper = createColumnHelper<scrapResultProps>();

export const columns = [
    columnHelper.accessor("kreamId", {
        header: "kream Id",
        cell: (row) => {
            return (
                <Link
                    target="_blank"
                    href={`http://kream.co.kr/products/${row.getValue()}`}
                    className="underline text-blue-600">
                    {row.getValue()}
                </Link>
            );
        },
    }),
    columnHelper.accessor("productCard", {
        cell: (row) => {
            return (
                <div className={` ${row.getValue() ? "bg-green-500" : "bg-rose-500"} text-white`}>
                    {row.getValue() ? "O" : "X"}
                </div>
            );
        },
    }),
    columnHelper.accessor("tradingVolume", {
        header: "Trading Volume",
        cell: (row) => {
            return (
                <div className={` ${row.getValue() ? "bg-green-500" : "bg-rose-500"} text-white`}>
                    {row.getValue() ? "O" : "X"}
                </div>
            );
        },
    }),
    columnHelper.accessor("bridge", {
        header: "Bridge",
        cell: (row) => {
            return (
                <div className={` ${row.getValue() ? "bg-green-500" : "bg-rose-500"} text-white`}>
                    {row.getValue() ? "O" : "X"}
                </div>
            );
        },
    }),
    columnHelper.accessor("buyAndSell", {
        header: "buy And Sell",
        cell: (row) => {
            return (
                <div className={` ${row.getValue() ? "bg-green-500" : "bg-rose-500"} text-white`}>
                    {row.getValue() ? "O" : "X"}
                </div>
            );
        },
    }),
    columnHelper.accessor("error", {
        header: "error",
        cell: (props) => {
            const error = props.row.original.error;
            const isFailed = error.includes("success") ? false : true;
            return <div className={`${isFailed && "font-bold"}`}>{props.getValue()}</div>;
        },
    }),
];
