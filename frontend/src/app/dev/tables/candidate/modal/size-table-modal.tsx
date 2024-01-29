"use client";

import BaseModal from "./modal";
import { useState, useMemo } from "react";

const enable = "bg-main-black text-white";
const disable = "bg-light-gray";

export type sizeProps = {
    meta: sizeMetaProps;
    sizeData: { [key: string]: sizeRowDataProps[] };
};

export type sizeMetaProps = {
    shop: string[];
    price: { [key: string]: number };
    size: sizeRowDataProps[];
};

export type sizeRowDataProps = {
    size: string;
    korSize: string;
    updatedAt: string;
};

const SizeTableModal = ({
    initShopName,
    size,
    isOpen,
    setIsOpen,
}: {
    initShopName: string;
    size: sizeProps;
    isOpen: boolean;
    setIsOpen: (v: boolean) => void;
}) => {
    const closeModal = () => setIsOpen(false);
    const shopNameArr = size.meta.shop;
    const sizeArr = size.meta.size;

    const [selectedShopName, setSelectedShopName] = useState<string[]>([initShopName]);

    const initSize = initShopName == "all" ? size.meta.size : size.sizeData[initShopName];
    const [selectedSize, setSelectedSize] = useState<sizeRowDataProps[]>(initSize);

    const handleAllShop = () => {
        setSelectedSize(sizeArr);
        setSelectedShopName(shopNameArr);
        return;
    };

    const handleShop = (shop: string) => {
        setSelectedSize(size.sizeData[shop]);
        setSelectedShopName([shop]);
    };

    const content = (
        <div className="min-h-[400px] text-base">
            <div className="pt-4 pb-2 text-xl">사이트</div>
            <div className="grid grid-cols-5 w-full text-center bg-light-gray border">
                <button
                    onClick={handleAllShop}
                    className={`${shopNameArr.length === selectedShopName.length ? enable : disable} py-2 `}>
                    All
                </button>
                {shopNameArr.map((v) => (
                    <button
                        onClick={() => handleShop(v)}
                        key={v}
                        className={`${selectedShopName.includes(v) ? enable : disable} py-2 `}>
                        <div>{v}</div>
                        <div>({size.meta.price[v].toLocaleString()})</div>
                    </button>
                ))}
            </div>
            <div className="pt-4 pb-2 text-xl">사이즈</div>
            <div className="grid grid-cols-5 w-full text-center bg-light-gray border">
                {sizeArr.map((s1) => {
                    const s2 = selectedSize.find((v) => v.korSize == s1.korSize);
                    return s2 ? (
                        <button key={`${s2.korSize}`} className="py-2 focus:bg-main-black focus:text-deep-gray">
                            <div>{s2.korSize}</div>
                            <span className="text-sm">({s2.size})</span>

                            <div className="text-xs">{s2.updatedAt}</div>
                        </button>
                    ) : (
                        <button
                            key={`${s1.korSize}`}
                            className="py-2 focus:bg-main-black focus:text-deep-gray disabled:bg-rose-100"
                            disabled={true}>
                            <div>{s1.korSize}</div>
                        </button>
                    );
                })}
            </div>
        </div>
    );

    return BaseModal({
        content: content,
        isOpen: isOpen,
        closeModal: closeModal,
    });
};

export default SizeTableModal;
