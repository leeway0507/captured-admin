"use client";
import Link from "next/link";
import Image from "next/image";
import { useState } from "react";
import envJson from "@/app/env.json";

const childClass = "border w-[130px] 2xl:w-[180px] h-[130px] 2xl:h-[180px] flex-center";

const BrandList = () => {
    const brandsArray = envJson.NEXT_PUBLIC_BRAND_ARRAY!;
    return (
        <div className="grid grid-cols-6 gap-2">
            {brandsArray.map((brandObj: { label: string; value: string }, idx: number) => {
                // brandName과 valueName을 쓰는 이유
                // adidas originals로 검색하면 결과가 종합적으로 나오지 않으므로 adidas로 검색하기 위함.
                const brandName = brandObj.label;
                const brandNameBar = brandName.replaceAll(" ", "-");
                const searchParam = brandObj.value;
                return (
                    <Link
                        href={`cost-table/brandName/${searchParam}`}
                        key={idx}
                        className={`flex bg-main-black  rounded-md relative `}>
                        <div className={`relative ${childClass}  z-20 bg-main-black hover:hidden`}>
                            <Image
                                src={`/brands/white/${brandNameBar}-white-logo.png`}
                                alt={brandNameBar}
                                fill
                                sizes="200px"
                                className="scale-[85%]"
                            />
                        </div>
                        <div className={`absolute inset-0 text-center text-white ${childClass}`}>{brandName}</div>
                    </Link>
                );
            })}
        </div>
    );
};

export default BrandList;
