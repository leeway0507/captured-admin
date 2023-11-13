"use client";
import Image from "next/image";
import Link from "next/link";
import KreamDetailModal from "./modal";
import { useEffect, useState } from "react";
import { getKreamProductCardList, getKreamProductSizeInfo } from "../[...slug]/fetch";
import { kreamTableRawDataProps } from "../[...slug]/table/type";

interface productSizeProps {
    kreamProductSize: string;
    buy: number;
    sell: number;
    count: number;
    min: number;
    median: number;
    max: number;
    lightening: number;
}

const Page = (kreamI: number, cos: number) => {
    const kreamId = 26344;
    const cost = 100000;
    const [isOpen, setIsOpen] = useState(true);
    const closeModal = () => setIsOpen(false);

    const [kreamProductCard, setKreamProductCard] = useState<kreamTableRawDataProps | undefined>(undefined);
    const [kreamProductSize, setKreamProductSize] = useState<productSizeProps[] | undefined>(undefined);
    const [scrapDate, setScrapDate] = useState<string[] | undefined>(undefined);

    useEffect(() => {
        getKreamProductCardList("kreamId", String(kreamId)).then((res) => {
            setKreamProductCard(res.data[0]);
        });
        getKreamProductSizeInfo("kreamId", String(kreamId)).then((res) => {
            setKreamProductSize(res.data.sizeData);
            setScrapDate(res.data.scrapDate);
        });
    }, []);

    const NotFoundModal = KreamDetailModal({
        content: (
            <div className="flex-center h-full w-full text-2xl text-sub-black underline grow">
                해당 정보가 없습니다.
            </div>
        ),
        isOpen: isOpen,
        closeModal: closeModal,
    });

    if (kreamProductCard === undefined) return NotFoundModal;
    if (scrapDate === undefined) return NotFoundModal;
    if (kreamProductSize === undefined) return NotFoundModal;

    const content = (
        <div className="flex flex-col">
            <div className="text-2xl bold text-main-black">제품 정보</div>
            <div className="flex-center pb-4">
                <div className="relative h-[100px] w-[180px] ">
                    <Image
                        src={kreamProductCard.kreamProductImgUrl}
                        alt={kreamProductCard.kreamProductName}
                        fill
                        style={{ objectFit: "cover" }}
                    />
                </div>
                <div className="flex-center">
                    <div className="grid grid-flow-row auto-rows-max gap-1">
                        <div className="grid grid-cols-5 gap-4">
                            <div className="col-span-1">제품명</div>
                            <div className="col-span-4">{kreamProductCard.kreamProductName}</div>
                        </div>
                        <div className="grid grid-cols-5 gap-4">
                            <div>제품 아이디</div>
                            <div>{kreamProductCard.productId}</div>
                        </div>
                        <div className="grid grid-cols-5 gap-4">
                            <div>크림 아이디</div>
                            <Link
                                href={`https://kream.co.kr/products/${kreamProductCard.kreamId}`}
                                target="_blank"
                                rel="noreferrer"
                                className="underline text-blue-700 pointer-cursor">
                                {kreamProductCard.kreamId}
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
            <div className="py-4">
                <div className="text-2xl bold text-main-black">사이즈 정보</div>
                <div className="flex text-base w-full">
                    <div>
                        <span>스크랩 날짜 : </span>
                        <span>
                            {scrapDate[0]?.replace("T00:00:00", "")} - {scrapDate[1]?.replace("T00:00:00", "")}
                        </span>
                    </div>
                    <div>
                        <span className="ps-4">제품 원가 : </span>
                        <span className="underline">{cost.toLocaleString()}원 </span>
                    </div>
                </div>

                <div className="w-full py-4">
                    <div className="grid grid-cols-7 gap-2 text-center py-2 odd:bg-light-gray font-bold">
                        <div>size</div>
                        <div>count(⚡️)</div>
                        <div>buy</div>
                        <div>sell</div>
                        <div>min</div>
                        <div>median</div>
                        <div>max</div>
                    </div>

                    {kreamProductSize.map((info) => {
                        const buyGap = info.buy - cost;
                        const minGap = info.min - cost;
                        const medianGap = info.median - cost;
                        const maxGap = info.max - cost;

                        const plus = "text-green-500 text-xs";
                        const minus = "text-red-500 text-xs";

                        const profit = (gap: number) => (
                            <div className={gap > 0 ? plus : minus}>{gap > 0 && `(+${gap.toLocaleString()})`}</div>
                        );

                        return (
                            <div
                                key={info.kreamProductSize}
                                className="grid grid-cols-7 gap-2 text-center py-2 odd:bg-light-gray">
                                <div>{info.kreamProductSize}</div>
                                <div>
                                    {info.count}({info.lightening})
                                </div>
                                <div className="flex-center flex-col">
                                    {info.buy.toLocaleString()}
                                    {profit(buyGap)}
                                </div>
                                <div className="border-r border-blue-black h-full">{info.sell.toLocaleString()}</div>
                                <div>
                                    {info.min.toLocaleString()}
                                    {profit(minGap)}
                                </div>
                                <div>
                                    {info.median.toLocaleString()}
                                    {profit(medianGap)}
                                </div>
                                <div>
                                    {info.max.toLocaleString()}
                                    {profit(maxGap)}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );

    return KreamDetailModal({
        content: content,
        isOpen: isOpen,
        closeModal: closeModal,
    });
};

export default Page;
