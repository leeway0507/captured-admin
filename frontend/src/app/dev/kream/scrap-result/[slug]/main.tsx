"use client";
import ScrapResultTable from "./table/scrap-result-table";
import Link from "next/link";
import { handleProductDtailSubmit } from "../../product-detail";
import { useRef, useState, useEffect } from "react";
import { scrapingProps } from "../../product-detail";
import { useRouter } from "next/navigation";
import { insertScarpToDB } from "../../fetch";
import { toast } from "react-toastify";

//css
const restartBtn =
    "black-bar-with-disabled p-4 text-xl disabled:bg-light-gray disabled:border disabled:border-main-black disabled:cursor-not-allowed disabled:text-main-black";

const createTableData = (
    scrapPlan: [string, any][],
    kreamProductCardList: Number[],
    kreamTradingVolumeList: Number[],
    kreamBuyandSellList: Number[],
    kreamProductBridgeList: Number[]
) => {
    return scrapPlan.map(([kreamIdStr, error]: [string, string]) => {
        const kreamId = Number(kreamIdStr);

        const tableData = {
            kreamId,
            productCard: false,
            tradingVolume: false,
            buyAndSell: false,
            bridge: false,
            error,
        };

        if (kreamProductCardList.includes(kreamId)) {
            tableData.productCard = true;
        }
        if (kreamTradingVolumeList.includes(kreamId)) {
            tableData.tradingVolume = true;
        }
        if (kreamBuyandSellList.includes(kreamId)) {
            tableData.buyAndSell = true;
        }
        if (kreamProductBridgeList.includes(kreamId)) {
            tableData.bridge = true;
        }
        return tableData;
    });
};

export default function ScrapResult({ fetchData }: { fetchData: any }) {
    const {
        scrap_name: scrapName,
        scrap_result: scrapResult,
        brand: brandName,
        kream_product_card: kreamProductCard,
        kream_trading_volume: kreamTradingVolume,
        kream_buy_and_sell: kreamBuyandSell,
        kream_product_bridge: kreamProductBridge,
        db_update: dbUpdate,
        num_process: numProcess,
        ref_product_card: refProductCard,
        ...res
    } = fetchData;

    const scrapPlan: [string, string][] = Object.entries(scrapResult);
    const scrapSuccess = scrapPlan.filter(([key, value]) => value.includes("success"));
    const scrapFailed = scrapPlan.filter(([key, value]) => !value.includes("success") && value !== "not_scrap");

    const tableData = createTableData(
        scrapPlan,
        kreamProductCard.kream_id_list,
        kreamTradingVolume.kream_id_list,
        kreamBuyandSell.kream_id_list,
        kreamProductBridge.kream_id_list
    );

    const submitRef = useRef<HTMLButtonElement>(null);
    const [configState, setConfigState] = useState<scrapingProps>({
        brandName,
        numProcess: numProcess,
        kreamIds: scrapFailed
            .reduce((acc, [kreamId, error]) => {
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

    return (
        <div className="flex flex-col gap-4 max-w-3xl mx-auto">
            <div className="text-3xl pt-8 w-full border-b-2 pb-2">
                제품 상세정보 수집결과
                <span className="ps-2 text-2xl">({scrapName})</span>
            </div>
            <div className="pt-4 pb-2 grid text-xl grid-flow-col ">
                <div>수집 브랜드 </div>
                <div>{brandName}</div>
                <div>실행 프로세스</div>
                <div>{numProcess} 개</div>
                <div>참고 제품 정보</div>
                <div className="text-xl">{refProductCard.slice(0, 10)}...</div>
            </div>
            <div className="border pt-4 px-4 text-xl grid grid-rows-2 bg-slate-50">
                <div className="grid grid-cols-8 mb-2 border-b pb-2">
                    <div className="text-blue-600">계획</div>
                    <div className="text-blue-600">{scrapPlan.length} 건</div>
                    <div className="text-green-600">성공</div>
                    <div className="text-green-600">{scrapSuccess.length} 건</div>
                    <div className="text-rose-600">실패</div>
                    <div className="text-rose-600">{scrapFailed.length} 건</div>
                    <div>미실행</div>
                    <div>{scrapPlan.length - (scrapSuccess.length + scrapFailed.length)} 건</div>
                </div>
                <div className="grid grid-cols-8 text-lg text-sub-black">
                    <div>세부정보</div>
                    <div>{kreamProductCard.len} 건</div>
                    <div>거래량</div>
                    <div>{kreamTradingVolume.len} 건</div>
                    <div>판매구매</div>
                    <div>{kreamBuyandSell.len} 건</div>
                    <div>브릿지</div>
                    <div>{kreamProductBridge.len} 건</div>
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
                        {configState.kreamIds.split(",").filter((v) => v !== "").length} 건
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
                        handleProductDtailSubmit(configState, setReStartScrapName, enableButton, disableButton)
                    }
                    className={`${restartBtn}`}
                    disabled={scrapFailed.length === 0}>
                    {scrapFailed.length === 0 ? "실패 목록 없음" : "실패 목록 재실행"}
                </button>
                <button
                    className="black-bar-with-disabled flex-right p-2 text-lg"
                    onClick={() => handleDB(scrapName)}
                    disabled={dbUpdate}>
                    {" "}
                    {dbUpdate ? "DB 넣기 완료" : "DB에 넣기"}
                </button>
                <Link href="/dev/kream/scrap-result/result-list" className="black-bar p-4 text-lg">
                    돌아가기
                </Link>
            </div>
        </div>
    );
}
