"use client";
import Link from "next/link";
import Image from "next/image";
import { useState } from "react";

const childClass = "border w-[130px] 2xl:w-[180px] h-[130px] 2xl:h-[180px] flex-center";

const BrandList = () => {
    const brandsArray = JSON.parse(process.env.NEXT_PUBLIC_BRAND_ARRAY!);

    const [hoveredIndex, setHoveredIndex] = useState<Number | null>(null);

    const handleMouseEnter = (index: Number | null) => {
        setHoveredIndex(index);
    };

    const handleMouseLeave = () => {
        setHoveredIndex(null);
    };
    return (
        <div className="grid grid-cols-6 gap-1">
            {brandsArray.map((brandName: string, idx: number) => {
                const brandNameBar = brandName.replaceAll(" ", "-");
                return (
                    <Link
                        href={`cost-table/brandName/${brandNameBar}`}
                        key={idx}
                        className={`flex bg-main-black hover:text-white py-1 transition-all duration-300 ease-in rounded-md`}
                        onMouseEnter={() => handleMouseEnter(idx)}
                        onMouseLeave={handleMouseLeave}>
                        <div
                            className={`relative ${childClass}  ${
                                idx === hoveredIndex ? "hidden" : "display scale-[85%]"
                            }`}>
                            <Image
                                src={`/brands/white/${brandNameBar}-white-logo.png`}
                                alt={brandNameBar}
                                fill
                                sizes="200px"
                            />
                        </div>
                        <div className={`text ${childClass}  ${idx === hoveredIndex ? "display" : "hidden"}`}>
                            {brandName}
                        </div>
                    </Link>
                );
            })}
        </div>
    );
};

export default BrandList;
