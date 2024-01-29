"use client";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { getShopPageReportAll } from "../../fetch-report";

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

export default function ShopProductPage() {
    const router = useRouter();
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const { status, data } = await getShopPageReportAll();
            if (status === 200) {
                setData(data);
            }
        };
        fetchData();
    }, []);

    const openDetailOrderToggle = (e: any) => {
        const fileName = e.currentTarget.getAttribute("scrap-name");
        router.push(`/dev/shop/report/page/${fileName}`);
    };
    return (
        <div className="flex flex-col w-full">
            <div className="grid">
                <div className="grid grid-cols-2 pt-8 pb-4 border-b">
                    <div className={`${header}`}>순번</div>
                    <div className={`${header}`}>파일명</div>
                </div>
                {data.map((d, idx) => (
                    <div
                        className={`${item} ${isOdd(idx) && "bg-light-gray"}`}
                        key={idx}
                        scrap-name={d}
                        onClick={openDetailOrderToggle}>
                        <div>{idx + 1}</div>
                        <div>{d}</div>
                    </div>
                ))}
            </div>
        </div>
    );
}
