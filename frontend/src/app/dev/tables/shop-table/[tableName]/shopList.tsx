"use client";
import Link from "next/link";
import Image from "next/image";
import { useState } from "react";

const childClass = "w-[130px] 2xl:w-[180px] h-[130px] 2xl:h-[180px] flex-center";

const ShopList = ({ tableType }: { tableType: string }) => {
    const shopArray = JSON.parse(process.env.NEXT_PUBLIC_SHOP_ARRAY!);

    return (
        <div className="grid grid-cols-6 gap-1">
            {shopArray.map((shopName: string, idx: number) => {
                const shopNameBar = shopName.replaceAll("-", "_");
                const searchParams = new URLSearchParams({ tableType, searchType: "shop-name", value: shopNameBar });
                return (
                    <Link
                        rel="noreferer"
                        target="_blank"
                        href={`${tableType}/table?${searchParams}`}
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
