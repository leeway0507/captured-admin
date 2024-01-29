"use client";
import ScrapResultTable from "./table/scrap-result-table";
import Link from "next/link";
import { handleProductDtailSubmit } from "../../platform-page";
import { useRef, useState, useEffect } from "react";
import { scrapingProps } from "../../platform-page";
import { useRouter } from "next/navigation";
import { insertPlatformPageData } from "../../fetch-report";
import { toast } from "react-toastify";

//css
const restartBtn =
    "black-bar-with-disabled p-4 text-xl disabled:bg-light-gray disabled:border disabled:border-main-black disabled:cursor-not-allowed disabled:text-main-black";

const createTableData = (
    job: string[],
    kreamProductCardList: string[],
    kreamTradingVolumeList: string[],
    kreamBuyandSellList: string[]
) => {
    return job.map((v, i) => {
        return {
            kreamId: v,
            productCard: kreamProductCardList[i],
            tradingVolume: kreamTradingVolumeList[i],
            buyAndSell: kreamBuyandSellList[i],
        };
    });
};

export default function ScrapResult({ fetchData }: { fetchData: any }) {
    const {
        scrap_time: scrapTime,
        num_of_plan: numOfPlan,
        job: job,
        folder_name: folderName,
        product_detail: ProductDetail,
        trading_volume: TradingVolume,
        buy_and_sell: BuyandSell,
        db_update: dbUpdate,
        num_processor: numProcess,
        ...res
    } = fetchData;

    var scrapSuccess = [];
    var scrapFailed = [];
    for (let i = 0; i < numOfPlan; i++) {
        if (
            ProductDetail[i].includes("success") &&
            TradingVolume[i].includes("success") &&
            BuyandSell[i].includes("success")
        ) {
            scrapSuccess.push(job[i]);
        } else {
            scrapFailed.push(job[i]);
        }
    }

    const tableData = createTableData(job, ProductDetail, TradingVolume, BuyandSell);

    const submitRef = useRef<HTMLButtonElement>(null);
    const [configState, setConfigState] = useState<scrapingProps>({
        searchType: "kreamId",
        numProcess: numProcess,
        searchValue: scrapFailed
            .reduce((acc, kreamId) => {
                return acc + "," + kreamId;
            }, "")
            .replace(",", ""),
    });

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

    const [newScrapName, setNewScrapName] = useState("");
    const router = useRouter();

    useEffect(() => {
        if (newScrapName === "") return;
        router.push(`/dev/kream/report/page/${newScrapName}`);
    }, [newScrapName, router]);

    const handleDB = async (searchValue: string, scrapName: string) => {
        await insertPlatformPageData(searchValue, scrapName).then((res) => {
            if (res.status === 200) {
                toast.success("DB 넣기 성공!");
            } else {
                toast.error("DB 넣기 실패!");
            }
        });
    };

    return (
        <div className="flex flex-col gap-4 max-w-3xl mx-auto">
            <div className="text-3xl pt-8 w-full border-b-2 pb-2">
                제품 상세정보 수집결과
                <span className="ps-2 text-2xl">({scrapTime})</span>
            </div>
            <div className="pt-4 pb-2 grid text-xl grid-flow-col ">
                <div>수집 브랜드 </div>
                <div>{folderName}</div>
                <div>실행 프로세스</div>
                <div>{numProcess} 개</div>
            </div>
            <div className="border pt-4 px-4 text-xl grid grid-rows-2 bg-slate-50">
                <div className="grid grid-cols-8 mb-2 border-b pb-2">
                    <div className="text-blue-600">계획</div>
                    <div className="text-blue-600">{numOfPlan} 건</div>
                    <div className="text-green-600">성공</div>
                    <div className="text-green-600">{scrapSuccess.length} 건</div>
                    <div className="text-rose-600">실패</div>
                    <div className="text-rose-600">{scrapFailed.length} 건</div>
                    <div>미실행</div>
                    <div>{numOfPlan - (scrapSuccess.length + scrapFailed.length)} 건</div>
                </div>
                <div className="grid grid-cols-8 text-lg text-sub-black">
                    <div>세부정보</div>
                    <div>{ProductDetail.len} 건</div>
                    <div>거래량</div>
                    <div>{TradingVolume.len} 건</div>
                    <div>판매구매</div>
                    <div>{BuyandSell.len} 건</div>
                </div>
            </div>
            <div>
                <div className="text-3xl py-4">수집 목록 결과</div>
                <ScrapResultTable tableData={tableData} />
            </div>

            <div className="flex gap-4 w-full text-lg py-8">
                <div className="flex flex-col">
                    <div>재실행 예정 </div>
                    <div className="flex-center grow bg-white py-2 border border-main-black">
                        {configState.searchValue.split(",").filter((v) => v !== "").length} 건
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
                    onClick={() => handleProductDtailSubmit(configState, setNewScrapName, enableButton, disableButton)}
                    className={`${restartBtn}`}
                    disabled={scrapFailed.length === 0}>
                    {scrapFailed.length === 0 ? "실패 목록 없음" : "실패 목록 재실행"}
                </button>
                <button
                    className="black-bar-with-disabled flex-right p-2 text-lg"
                    onClick={() => handleDB(folderName, scrapTime)}
                    disabled={dbUpdate}>
                    {" "}
                    {dbUpdate ? "DB 넣기 완료" : "DB에 넣기"}
                </button>
                <Link href="/dev/kream/report/all" className="black-bar p-4 text-lg">
                    돌아가기
                </Link>
            </div>
        </div>
    );
}
