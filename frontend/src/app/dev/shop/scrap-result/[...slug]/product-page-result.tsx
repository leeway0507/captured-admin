"use client";
import Link from "next/link";
import { useRef, useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";
import { insertScrapPageToDB } from "../../fetch";
import { handleScrapProductPage, searchProps } from "../../shop-card-page";

interface fetchDataProps {
    num_of_plan: string;
    scrap_time: string;
    scrap_result: scrapResultProps[];
    db_update: boolean;
    num_process: number;
}

interface scrapResultProps {
    shop_product_card_id: number;
    shop_name: string;
    brand_name: string;
    url: string;
    status: string;
    product_id: string;
    product_name: string;
}
interface scrapingProps {
    scrapList: scrapResultProps[];
    numProcess: number;
}

//css
const restartBtn =
    "black-bar-with-disabled p-4 text-xl disabled:bg-light-gray disabled:border disabled:border-main-black disabled:cursor-not-allowed disabled:text-main-black";

export default function ProductPageResult({ fetchData }: { fetchData: fetchDataProps }) {
    const {
        num_of_plan: numOfPlan,
        scrap_time: scrapTime,
        scrap_result: scrapResult,
        db_update: dbUpdate,
        num_process: numProcess,
    } = fetchData;

    const submitRef = useRef<HTMLButtonElement>(null);

    const scrapSuccess = scrapResult.filter((obj) => obj.status === "success");
    const scrapFailed = scrapResult.filter((obj) => obj.status !== "success");

    const [configState, setConfigState] = useState<searchProps>({
        numProcess: numProcess,
        searchType: "shopProductCardId",
        content: scrapFailed
            .reduce((acc, cur) => {
                return acc + "," + cur.shop_product_card_id;
            }, "")
            .replace(",", ""),
    });

    const [reStartScrapName, setReStartScrapName] = useState("");
    const router = useRouter();

    useEffect(() => {
        if (reStartScrapName === "") return;
        router.push(`/dev/shop/scrap-result/page/${reStartScrapName}`);
    }, [reStartScrapName, router]);

    const handleDB = async (scrapDate: string) => {
        await insertScrapPageToDB(scrapDate).then((res) => {
            console.log(res);
            if (res.status === 200) {
                toast.success("DB 넣기 성공!");
            } else {
                toast.error("DB 넣기 실패!");
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
        <div className="flex flex-col gap-4 max-w-3xl mx-auto py-8 ">
            <div className="py-2">
                <span className="text-3xl">제품 상세정보 수집결과</span>
                <span className="text-2xl">({scrapTime})</span>
            </div>
            <div className="p-4 text-xl bg-gray-100">
                <div className="grid grid-cols-8 border-b mb-4 pb-2">
                    <div className="text-blue-600">계획</div>
                    <div className="text-blue-600">{numOfPlan} 건</div>
                    <div className="text-green-600">성공</div>
                    <div className="text-green-600">{scrapSuccess.length} 건</div>
                    <div className="text-rose-600">실패</div>
                    <div className="text-rose-600">{scrapFailed.length} 건</div>
                    <div>미실행</div>
                    <div>{Number(numOfPlan) - (scrapSuccess.length + scrapFailed.length)} 건</div>
                </div>
            </div>
            <div className="text-3xl pb-2">수집 목록 결과</div>
            <div className="py-4 pb-12 bg-gray-100">
                <div className="grid grid-cols-6 border-b mb-4 pb-2 gap-2 text-lg py-2 text-center">
                    <div>SHOP_CARD_ID</div>
                    <div>스토어</div>
                    <div>브랜드</div>
                    <div>제품코드</div>
                    <div className="col-span-2">결과</div>
                </div>
                {scrapResult.map((obj, idx) => (
                    <div
                        key={obj.shop_product_card_id}
                        className="grid grid-cols-6 border-b mb-4 pb-2 gap-2 py-2 text-center">
                        <Link
                            href={obj.url}
                            className="text-blue-700 cursor-pointer underline"
                            target="_blank"
                            rel="noreferrer">
                            {obj.shop_product_card_id}
                        </Link>
                        <div>{obj.shop_name}</div>
                        <div>{obj.brand_name}</div>
                        <div>{obj.product_id}</div>
                        <div className="col-span-2">{obj.status}</div>
                    </div>
                ))}
            </div>
            <div className="flex gap-4 w-full text-lg">
                <div className="flex flex-col">
                    <div>재실행 예정 </div>
                    <div className="flex-center grow bg-white py-2 border border-main-black">
                        {scrapFailed.length} 건
                    </div>
                </div>
                <div className="flex flex-col">
                    <label htmlFor="numProcess">재실행 프로세스 수</label>
                    <input
                        type="text"
                        id="numProcess"
                        onChange={(e) => setConfigState({ ...configState, numProcess: Number(e.target.value) })}
                        value={configState.numProcess}
                        className="border border-main-black p-2"
                    />
                </div>
                <button
                    ref={submitRef}
                    onClick={() =>
                        handleScrapProductPage(configState, setReStartScrapName, enableButton, disableButton)
                    }
                    className={`${restartBtn}`}
                    disabled={scrapFailed.length === 0}>
                    {scrapFailed.length === 0 ? "실패 목록 없음" : "실패 목록 재실행"}
                </button>
                <button
                    className="black-bar-with-disabled flex-right p-2 text-lg"
                    onClick={() => handleDB(scrapTime)}
                    disabled={dbUpdate}>
                    {" "}
                    {dbUpdate ? "DB 넣기 완료" : "DB에 넣기"}
                </button>
                <Link href="/dev/shop/scrap-result/result-list" className="black-bar p-4 text-lg">
                    돌아가기
                </Link>
            </div>
        </div>
    );
}
