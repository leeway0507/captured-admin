"use client";
import Link from "next/link";
import { CloseKreamBrowser } from "./fetch-scrap";
import PlatformList from "./platform-list";
import PlatformPage from "./platform-page";
import ReproduceReport from "./reproduce-report";
import { toast } from "react-toastify";
export default function Main() {
    const handleCloseBrowser = async () => {
        const res = await CloseKreamBrowser().then((res) => {
            if (res.status === 200) {
                alert("브라우저 재실행 성공");
            } else {
                toast.error(`${res.status} 에러 발생`);
            }
        });
    };

    return (
        <div className="flex flex-col mx-auto">
            <div className="w-full flex-right py-4 gap-8">
                <Link href="/dev/kream/scrap-result/result-list">
                    <button className="black-bar w-[300px] p-4 text-xl">수집결과 보기</button>
                </Link>
                <button className="black-bar w-[300px] p-4 text-xl" onClick={handleCloseBrowser}>
                    브라우저 재실행
                </button>
            </div>
            <div className="bg-slate-50 py-16 px-8 ">
                <div className="text-3xl pb-4 ">크림 브랜드 수집</div>
                <PlatformList />
            </div>
            <div className="bg-slate-100 py-16 px-8">
                <div className="text-3xl pb-4 ">크림 상세 제품 수집</div>
                <PlatformPage />
            </div>
            {/* <div className="bg-slate-50 py-16 px-8">
                <div className="text-3xl ">수집 결과 재생산</div>
                <ReproduceReport />
            </div> */}
        </div>
    );
}
