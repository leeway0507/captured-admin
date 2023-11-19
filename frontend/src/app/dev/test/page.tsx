"use client";

import Data from "./data.json";
import { useMemo, useState } from "react";

const enable = "bg-main-black text-white";
const disable = "bg-light-gray";

export interface productCardProps {
    shopProductCardId: number;
    shopProductName: string;
    shopProductImgUrl: string;
    productUrl: string;
    shopName: string;
    brandName: string;
    productId: string;
    korPrice: number;
    usPrice: number;
    originalPriceCurrency: string;
    originalPrice: number;
    soldOut: boolean;
    candidate: number;
    updatedAt: string;
    coupon: number;
}
interface sizeInfoprops {
    shopProductCardId: number;
    shopProductSize: string;
    korProductSize: string;
    available: boolean;
    updatedAt: string;
}
interface accType {
    [key: string]: number[];
}

const createSizeDict = (sizeInfo: sizeInfoprops[]) => {
    return sizeInfo.reduce((acc: accType, cur) => {
        return {
            ...acc,
            [cur.korProductSize]: [
                ...(acc[cur.korProductSize] || []), // Preserve existing data
                cur.shopProductCardId,
            ],
        };
    }, {});
};

const Page = () => {
    const sizeInfo = Data.sizeInfo;
    const sizeDict = useMemo(() => createSizeDict(sizeInfo), [sizeInfo]);

    const sizeName = Object.keys(sizeDict);
    const shopName = Data.productInfo
        .map((obj) => obj.shopName)
        .filter((value, index, self) => {
            return self.indexOf(value) === index;
        });

    const [selectedSize, setSelectedSize] = useState<string[]>(sizeName);
    const [selectedShopName, setSelectedShopName] = useState<string[]>(shopName);
    const [selectedShopInfo, setSelectedShopInfo] = useState<productCardProps[]>(Data.productInfo);

    const handleAllShop = () => {
        setSelectedSize(sizeName);
        setSelectedShopName(shopName);
        setSelectedShopInfo(Data.productInfo);
        return;
    };

    const handleSize = (size: string) => {
        const ids = sizeDict[size];
        return setSelectedShopInfo(Data.productInfo.filter((obj) => ids.includes(obj.shopProductCardId)));
    };

    const handleShop = (shop: string) => {
        const shopInfo = Data.productInfo.find((obj) => obj.shopName === shop);

        if (shopInfo) setSelectedShopInfo([shopInfo]);

        const shopProductCardId = shopInfo?.shopProductCardId;
        const selectedSizes = Data.sizeInfo
            .filter((obj) => obj.shopProductCardId === shopProductCardId)
            .map((obj) => obj.korProductSize);
        setSelectedSize(selectedSizes);
        return setSelectedShopName([shop]);
    };

    return (
        <div className="w-screen h-screen flex-center">
            <div className="w-[800px] h-[600px] border border-main-black">
                <div className="grid grid-cols-6 w-full text-center bg-light-gray border">
                    {sizeName.map((v) => (
                        <button
                            onClick={() => handleSize(v)}
                            key={`${v}`}
                            className="py-2 focus:bg-main-black focus:text-deep-gray disabled:bg-rose-100"
                            disabled={!selectedSize.includes(v)}>
                            {v}
                        </button>
                    ))}
                </div>
                <div className="grid grid-cols-6 w-full text-center bg-light-gray border">
                    <button
                        onClick={handleAllShop}
                        className={`${shopName.length === selectedShopName.length ? enable : disable} py-2 `}>
                        All
                    </button>
                    {shopName.map((v) => (
                        <button
                            onClick={() => handleShop(v)}
                            key={v}
                            className={`${selectedShopName.includes(v) ? enable : disable} py-2 `}>
                            {v}
                        </button>
                    ))}
                </div>

                <div className="grid grid-cols-6 text-center ">
                    <div>스토어</div>
                    <div>스토어</div>
                    <div>스토어</div>
                    <div>스토어</div>
                    <div>스토어</div>
                    <div>스토어</div>
                </div>
                <div className="w-full">
                    {selectedShopInfo.map((obj, idx) => {
                        return (
                            <div key={idx} className="grid grid-cols-6 text-center">
                                <div>{obj.shopName}</div>
                                <div>{obj.shopName}</div>
                                <div>{obj.shopName}</div>
                                <div>{obj.shopName}</div>
                                <div>{obj.shopName}</div>
                                <div>{obj.shopName}</div>
                                <div></div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};

export default Page;
