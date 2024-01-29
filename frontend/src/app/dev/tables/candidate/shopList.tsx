"use client";
import Link from "next/link";
import { loadShopListName } from "../../shop/fetch-scrap";
import { useState, useEffect } from "react";

const childClass = "w-[130px] 2xl:w-[180px] h-[130px] 2xl:h-[180px] flex-center";

const ShopList = () => {
    const [shopArray, setShopArray] = useState<string[]>([""]);

    useEffect(() => {
        const d = async () => {
            var c = await loadShopListName();
            setShopArray(c.data);
        };

        d();
    }, []);

    return (
        <div className="grid grid-cols-6 gap-1">
            {shopArray.map((shopName: string, idx: number) => {
                const shopNameBar = shopName.replaceAll("-", "_");
                return (
                    <Link
                        rel="noreferer"
                        target="_blank"
                        href={`candidate/shop/${shopNameBar}`}
                        key={idx}
                        className={`flex bg-main-black hover:bg-white text-light-gray hover:text-main-black py-1 transition-all duration-300 ease-in rounded-md`}>
                        <div className={`text-lg  ${childClass} `}>{shopName}</div>
                    </Link>
                );
            })}
        </div>
    );
};

export default ShopList;
