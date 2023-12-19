"use client";
import Link from "next/link";
import Image from "next/image";
import { useState } from "react";

const childClass = "w-[130px] 2xl:w-[180px] h-[130px] 2xl:h-[180px] flex-center";

const ShopList = () => {
    const shopArray = JSON.parse(process.env.NEXT_PUBLIC_SHOP_ARRAY!);

    return (
        <div className="grid grid-cols-6 gap-1">
            {shopArray.map((shopName: string, idx: number) => {
                const shopNameBar = shopName.replaceAll("-", "_");
                return (
                    <Link
                        href={`candidate-table/shopName/${shopNameBar}`}
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
