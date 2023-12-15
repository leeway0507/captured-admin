"use client";
import Link from "next/link";
import { useRef, useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";
import { insertScarpToDB, deleteScrapList } from "../../fetch";
import { handleSubmit } from "../../shop-card-list";

interface scrapingProps {
    shopName: string;
    brandName: string;
    numProcess: number;
}

interface fetchDataProps {
    shop_name: string;
    scrap_time: string;
    scrap_result: object;
    brand_list: string[];
    db_update: boolean;
    num_process: number;
}

//css
const restartBtn =
    "black-bar-with-disabled p-4 text-xl disabled:bg-light-gray disabled:border disabled:border-main-black disabled:cursor-not-allowed disabled:text-main-black";

export default function ProductListResult({ fetchData }: { fetchData: fetchDataProps }) {
    const {
        shop_name: shopName,
        scrap_time: scrapTime,
        scrap_result: scrapResult,
        brand_list: brandList,
        db_update: dbUpdate,
        num_process: numProcess,
        ...res
    } = fetchData;

    const submitRef = useRef<HTMLButtonElement>(null);

    const scrapPlan = Object.entries(scrapResult);
    const scrapSuccess = scrapPlan.filter(([key, value]) => value === "success");
    const scrapFailed = scrapPlan.filter(([key, value]) => value !== "success" && value !== "not_scrap");

    const [configState, setConfigState] = useState<scrapingProps>({
        shopName,
        numProcess: numProcess,
        brandName: scrapFailed
            .reduce((acc, [brandName, error]) => {
                return acc + "," + brandName;
            }, "")
            .replace(",", ""),
    });

    const [reStartScrapName, setReStartScrapName] = useState("");
    const router = useRouter();

    useEffect(() => {
        if (reStartScrapName === "") return;
        router.push(`/dev/kream/scrap-result/${reStartScrapName}`);
    }, [reStartScrapName, router]);

    const handleDB = async (scrapName: string) => {
        await insertScarpToDB(scrapName).then((res) => {
            console.log(res);
            if (res.status === 200) {
                toast.success("DB 넣기 성공!");
            } else {
                toast.error("DB 넣기 실패!");
            }
        });
    };
    const handleDelete = async (scrapName: string) => {
        await deleteScrapList(scrapName).then((res) => {
            if (res.status === 200) {
                toast.success("삭제 성공");
                router.replace("/dev/shop/scrap-result/result-list");
            } else {
                toast.error("삭제 실패");
            }
        });
    };

    const enableButton = () => {
        if (submitRef.current) {
            submitRef.current.disabled = false;
        }
    };

    const disableButton = () => {
        if (submitRef.current) {
            submitRef.current.disabled = true;
        }
    };

    return (
        <div className="flex flex-col gap-4 max-w-3xl mx-auto py-8">
            <div className="py-2">
                <span className="text-3xl">제품 상세정보 수집결과</span>
                <span className="text-2xl">({`${scrapTime}-${shopName}`})</span>
            </div>
            <div className="p-4 text-xl bg-gray-100">
                <div className="grid grid-cols-8 border-b mb-4 pb-2">
                    <div className="text-blue-600">계획</div>
                    <div className="text-blue-600">{scrapPlan.length} 건</div>
                    <div className="text-green-600">성공</div>
                    <div className="text-green-600">{scrapSuccess.length} 건</div>
                    <div className="text-rose-600">실패</div>
                    <div className="text-rose-600">{scrapFailed.length} 건</div>
                    <div>미실행</div>
                    <div>{scrapPlan.length - (scrapSuccess.length + scrapFailed.length)} 건</div>
                </div>
            </div>
            <div className="py-4 pb-12">
                <div className="text-3xl pb-2">수집 목록 결과</div>
                <div className="grid grid-cols-2 border-b mb-4 pb-2 gap-2 text-xl py-2 text-center">
                    <div>브랜드명</div>
                    <div>결과</div>
                </div>
                {Object.entries(scrapResult).map(([brandName, status], idx) => (
                    <div key={idx} className="grid grid-cols-2 mb-4 pb-2 gap-2 text-center">
                        <div>{brandName}</div>
                        <div>{status}</div>
                    </div>
                ))}
            </div>
            <div className="flex gap-4 w-full text-xl">
                <div className="flex flex-col w-20">
                    <div>재실행 예정 </div>
                    <div className="flex-center grow bg-white py-2 border border-main-black">
                        {configState.brandName.split(",").filter((v) => v !== "").length} 건
                    </div>
                </div>
                <div className="flex flex-col w-20">
                    <label htmlFor="numProcess">재실행 프로세스 수</label>
                    <input
                        type="text"
                        id="numProcess"
                        onChange={(e) => setConfigState({ ...configState, numProcess: Number(e.target.value) })}
                        value={configState.numProcess}
                        className="border border-main-black p-2 "
                    />
                </div>
                <button
                    ref={submitRef}
                    onClick={() => handleSubmit(configState, setReStartScrapName, enableButton, disableButton)}
                    className={`${restartBtn}`}
                    disabled={scrapFailed.length === 0}>
                    {scrapFailed.length === 0 ? "실패 목록 없음" : "실패 목록 재실행"}
                </button>
                <button
                    className="black-bar-with-disabled flex-right p-2 text-xl"
                    onClick={() => handleDB(`${scrapTime}-${shopName}`)}
                    disabled={dbUpdate}>
                    {" "}
                    {dbUpdate ? "DB 넣기 완료" : "DB에 넣기"}
                </button>
                <button
                    className="black-bar bg-rose-700 flex-right p-2 text-xl"
                    onClick={() => handleDelete(`${scrapTime}-${shopName}`)}>
                    {" "}
                    수집 결과 삭제
                </button>
                <Link href="/dev/shop/scrap-result/result-list" className="black-bar p-4 text-xl">
                    돌아가기
                </Link>
            </div>
        </div>
    );
}
