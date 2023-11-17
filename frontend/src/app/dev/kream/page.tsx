"use client";
import { ReloadBrowser } from "./fetch";
import PrdoucCardList from "./product-card-list";
import ProductDetail from "./product-detail";
import ReproduceReport from "./reproduce-report";
import { toast } from "react-toastify";
export default function Main() {
    const handleReloadBrowser = async () => {
        const res = await ReloadBrowser().then((res) => {
            if (res.status === 200) {
                alert("브라우저 재실행 성공");
            } else {
                toast.error(`${res.status} 에러 발생`);
            }
        });
    };

    return (
        <div className="flex flex-col mx-auto">
            <div className="w-full flex-right py-4">
                <button className="black-bar w-[300px] p-4 text-xl" onClick={handleReloadBrowser}>
                    브라우저 재실행
                </button>
            </div>
            <div className="bg-slate-50 py-16 px-8 ">
                <div className="text-3xl ">크림 브랜드 수집</div>
                <PrdoucCardList />
            </div>
            <div className="bg-slate-100 py-16 px-8">
                <div className="text-3xl ">크림 상세 제품 수집</div>
                <ProductDetail />
            </div>
            <div className="bg-slate-50 py-16 px-8">
                <div className="text-3xl ">수집 결과 재생산</div>
                <ReproduceReport />
            </div>
        </div>
    );
}
