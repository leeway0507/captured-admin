"use client";
import Link from "next/link";
import { CloseCustomPageBrowser } from "./fetch";
import { toast } from "react-toastify";
import ShopCardList from "./shop-card-list";
import ShopCardPage from "./shop-card-page";

export default function Main() {
    const handleCloseBrowser = async () => {
        const res = await CloseCustomPageBrowser().then((res) => {
            if (res.status === 200) {
                alert("브라우저 종료 성공");
            } else {
                toast.error(`${res.status} 에러 발생`);
            }
        });
    };

    return (
        <div className="flex flex-col mx-auto">
            <div className="w-full flex-right py-4 gap-8">
                <Link href="/dev/shop/scrap-result/result-list">
                    <button className="black-bar w-[300px] p-4 text-xl">수집결과 보기</button>
                </Link>
                <button className="black-bar w-[300px] p-4 text-xl" onClick={handleCloseBrowser}>
                    브라우저 재실행
                </button>
            </div>
            <div className="bg-slate-50 px-8 ">
                <div className="text-3xl pt-8">Shop Product List</div>
                <ShopCardList />
            </div>
            <div className="bg-slate-50 px-8 ">
                <div className="text-3xl pt-8">Shop Product Page</div>
                <ShopCardPage />
            </div>
        </div>
    );
}
