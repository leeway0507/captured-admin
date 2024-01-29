"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { getPlatformListReportAll } from "../../fetch-report";

interface ScrapResultProps {
    brandName: string;
    scrapType: string;
    scrapAt: string;
}

//css
const header = "border-main-black text-center";
const item = "grid grid-cols-2 text-center py-3 link-animation text-sm";

const isOdd = (num: number) => {
    return num % 2 != 0;
};

export default function KreamList() {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const { status, data } = await getPlatformListReportAll();
            if (status === 200) {
                setData(data);
            }
        };
        fetchData();
    }, []);

    return (
        <div className="flex flex-col w-full">
            <div className="grid">
                <div className="grid grid-cols-2 pt-8 pb-4 border-b">
                    <div className={`${header}`}>순번</div>
                    <div className={`${header}`}>파일명</div>
                </div>
                {data.map((fileName, idx) => (
                    <Link
                        target="_blank"
                        rel="noreferrer"
                        className={`${item} ${isOdd(idx) && "bg-light-gray"}`}
                        key={idx}
                        href={`/dev/kream/report/list/${fileName}`}>
                        <div>{idx + 1}</div>
                        <div>{fileName}</div>
                    </Link>
                ))}
            </div>
        </div>
    );
}
