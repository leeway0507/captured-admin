"use client";

import BaseModal from "./modal";
import { useState, useMemo } from "react";

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
export interface sizeInfoprops {
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

const SizeTableModal = ({
    initShopName,
    sizeInfo,
    productInfo,
    isOpen,
    setIsOpen,
}: {
    initShopName: string;
    sizeInfo: sizeInfoprops[];
    productInfo: productCardProps[];
    isOpen: boolean;
    setIsOpen: (v: boolean) => void;
}) => {
    const closeModal = () => setIsOpen(false);

    const sizeDict = useMemo(() => createSizeDict(sizeInfo), [sizeInfo]);

    const sizeName = Object.keys(sizeDict);
    const shopName = productInfo
        .map((obj) => obj.shopName)
        .filter((value, index, self) => {
            return self.indexOf(value) === index;
        });

    const [selectedSize, setSelectedSize] = useState<string[]>(sizeName);
    const [selectedShopName, setSelectedShopName] = useState<string[]>([initShopName]);
    const [selectedShopInfo, setSelectedShopInfo] = useState<productCardProps[]>(productInfo);

    const handleSize = (size: string) => {
        const ids = sizeDict[size];
        return setSelectedShopInfo(productInfo.filter((obj) => ids.includes(obj.shopProductCardId)));
    };

    const handleAllShop = () => {
        setSelectedSize(sizeName);
        setSelectedShopName(shopName);
        setSelectedShopInfo(productInfo);
        return;
    };

    const handleShop = (shop: string) => {
        const shopInfo = productInfo.find((obj) => obj.shopName === shop);

        if (shopInfo) setSelectedShopInfo([shopInfo]);

        const shopProductCardId = shopInfo?.shopProductCardId;
        const selectedSizes = sizeInfo
            .filter((obj) => obj.shopProductCardId === shopProductCardId)
            .map((obj) => obj.korProductSize);
        setSelectedSize(selectedSizes);
        return setSelectedShopName([shop]);
    };

    const NotFoundModal = BaseModal({
        content: (
            <div className="flex-center h-full w-full text-2xl text-blue-700 underline grow">
                해당 정보와 일치하는 사이즈가 없습니다.
            </div>
        ),
        isOpen: isOpen,
        closeModal: closeModal,
    });

    if (sizeInfo === undefined) return NotFoundModal;

    const content = (
        <div className="min-h-[400px] text-base">
            <div className="pt-4 pb-2 text-xl">사이트</div>
            <div className="grid grid-cols-5 w-full text-center bg-light-gray border">
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
            <div className="pt-4 pb-2 text-xl">사이즈</div>
            <div className="grid grid-cols-5 w-full text-center bg-light-gray border">
                {sizeName.map((v) => (
                    <button
                        onClick={() => handleSize(v)}
                        key={`${v}`}
                        className="py-2 focus:bg-main-black focus:text-deep-gray disabled:bg-rose-100"
                        disabled={!selectedSize.includes(v)}>
                        <div>{v}</div>
                    </button>
                ))}
            </div>

            {/* <div className="grid grid-cols-5 text-center ">
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
                        <div key={idx} className="grid grid-cols-5 text-center">
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
            </div> */}
        </div>
    );

    return BaseModal({
        content: content,
        isOpen: isOpen,
        closeModal: closeModal,
    });
};

export default SizeTableModal;
