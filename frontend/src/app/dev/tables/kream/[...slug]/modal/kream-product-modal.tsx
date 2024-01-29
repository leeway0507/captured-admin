"use client";
import Image from "next/image";
import Link from "next/link";
import BaseModal from "./modal";
import { useEffect, useState } from "react";
import { getKreamProdCard, getKreamMarketPrice } from "../fetch";
import { kreamTableRawDataProps } from "../table/kream-table";

interface marketPriceProps {
    kreamProductSize: string;
    buy: number;
    sell: number;
    count: number;
    min: number;
    median: number;
    max: number;
    lightening: number;
}

const KreamProductModal = ({
    searchType,
    value,
    isOpen,
    setIsOpen,
    cost = 9000000,
}: {
    searchType: string;
    value: string;
    isOpen: boolean;
    setIsOpen: (v: boolean) => void;
    cost: number;
}) => {
    const closeModal = () => setIsOpen(false);

    const [kreamProductCard, setKreamProductCard] = useState<kreamTableRawDataProps | undefined>(undefined);
    const [kreamProductSize, setKreamProductSize] = useState<marketPriceProps[] | undefined>(undefined);
    const [scrapDate, setScrapDate] = useState<string | undefined>(undefined);

    useEffect(() => {
        getKreamProdCard(String(value)).then((res) => {
            setKreamProductCard(res.data[0]);
        });
        getKreamMarketPrice(String(value)).then((res) => {
            setKreamProductSize(res.data.data);
            setScrapDate(res.data.baseDate);
        });
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const NotFoundModal = BaseModal({
        content: (
            <div className="flex-center h-full w-full text-2xl text-blue-700 underline grow">
                <Link href={`https://kream.co.kr/search?keyword=${value}`} target="_blank" rel="noreferrer">
                    해당 정보({value})와 일치하는 크림 정보가 없습니다.
                </Link>
            </div>
        ),
        isOpen: isOpen,
        closeModal: closeModal,
    });

    if (kreamProductCard === undefined) return NotFoundModal;

    const sizeInfo = () => {
        if (scrapDate === undefined || kreamProductSize === undefined)
            return (
                <div className="flex-center h-full w-full text-2xl text-sub-black underline grow">
                    사이즈 정보가 없습니다.
                </div>
            );

        return (
            <div>
                <div className="flex text-base w-full">
                    <div>
                        <span>스크랩 기준일 : </span>
                        <span>{scrapDate.split("T")[0]} ~ NOW</span>
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
                                <div className="font-bold">
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
        );
    };

    const content = (
        <div className="flex flex-col">
            <div className="text-2xl bold text-main-black">제품 정보</div>
            <div className="flex-left pb-4">
                <div className="relative h-[100px] w-[180px] ">
                    <Link
                        href={`https://kream.co.kr/products/${kreamProductCard.kreamId}`}
                        target="_blank"
                        rel="noreferrer"
                        className="underline text-blue-700 pointer-cursor">
                        <Image
                            src={kreamProductCard.kreamProductImgUrl}
                            alt={kreamProductCard.kreamProductName}
                            fill
                            style={{ objectFit: "cover" }}
                        />
                    </Link>
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
                {sizeInfo()}
            </div>
        </div>
    );

    return BaseModal({
        content: content,
        isOpen: isOpen,
        closeModal: closeModal,
    });
};

export default KreamProductModal;
