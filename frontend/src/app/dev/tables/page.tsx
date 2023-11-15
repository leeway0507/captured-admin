"use client";
import { useRouter } from "next/navigation";

const box =
    "px-8 text-4xl border border-main-black rounded-lg h-[250px] flex-center hover:bg-main-black transition duration-500  hover:text-white cursor-pointer";

const Page = () => {
    const router = useRouter();
    return (
        <div className="flex-center w-full">
            <div className="grid grid-cols-3 gap-8">
                <div className={`${box}`} onClick={() => router.push("tables/candidate-table")}>
                    후보 테이블
                </div>
                <div className={`${box}`} onClick={() => router.push("tables/kream-table")}>
                    크림 테이블
                </div>
                <div className={`${box}`} onClick={() => router.push("tables/cost-table")}>
                    단가 테이블
                </div>
            </div>
        </div>
    );
};

export default Page;
