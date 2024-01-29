"use client";
import { useRouter } from "next/navigation";
import { useReducer, useRef, useEffect, useState } from "react";
import { ScrapShopList, loadShopListBrandName, loadShopListName } from "./fetch-scrap";
import { toast } from "react-toastify";
import Select from "react-select";
import ShopBrandSelect from "./shop-brand-select";

type scrapingProps = {
    shopName: string;
    brandName: string;
    numProcess: number;
};

const initialState = {
    shopName: "",
    brandName: "",
    numProcess: 1,
};

export default function ShopCardList() {
    const submitRef = useRef<HTMLButtonElement>(null);
    const [state, dispatch] = useReducer(reducer, initialState);
    const [reportName, setReportName] = useState("");

    const router = useRouter();

    // redirect to report page after scraping
    useEffect(() => {
        if (reportName === "") return;
        router.push(`/dev/shop/report/list/${reportName}`);
    }, [reportName, router, state.shopName]);

    return (
        <div className="flex pt-4 pb-24 gap-1 justify-between max-w-5xl">
            <ShopBrandSelect
                shopSelect={state.shopName}
                setShopSelect={(e) => dispatch({ type: "shopName", payload: e.value })}
                brandSelect={state.brandName}
                setBrandSelect={(e) => dispatch({ type: "brandName", payload: e })}
            />
            <div className="min-w-[150px] flex flex-col">
                <label htmlFor="numProcess">프로세스 수</label>
                <input
                    type="text"
                    name="numProcess"
                    id="numProcess"
                    onChange={(e) => {
                        e.target.value;
                        dispatch({ type: "numProcess", payload: e.target.value });
                    }}
                    value={state.numProcess}
                    className="border border-main-black h-[50px] rounded-md px-4"
                />
            </div>
            <button
                ref={submitRef}
                className="black-bar-with-disabled min-w-[150px] text-xl h-[100px] "
                onClick={() => handleSubmit(state, setReportName, submitRef)}>
                요청하기
            </button>
        </div>
    );
}
const reducer = (state: scrapingProps, action: any) => {
    switch (action.type) {
        case "shopName":
            return { ...state, shopName: action.payload };
        case "brandName":
            return { ...state, brandName: action.payload };
        case "numProcess":
            return { ...state, numProcess: action.payload };
        default:
            return state;
    }
};

export const handleSubmit = async (
    state: scrapingProps,
    setReportName: (scrapName: string) => void,
    Ref: React.RefObject<HTMLButtonElement>
) => {
    const enableButton = () => {
        if (Ref.current) {
            Ref.current.disabled = false;
        }
    };

    const disableButton = () => {
        if (Ref.current) {
            Ref.current.disabled = true;
        }
    };

    if (state.brandName === "") {
        return toast.error("브랜드 네임을 입력해주세요.");
    }
    if (state.shopName === "") {
        return toast.error("스크랩할 샵을 선택하세요.");
    }

    const start = confirm(`브랜드네임 [${state.brandName}]이 맞으면 시작합니다.`);

    if (!start) {
        return;
    }

    disableButton();
    await ScrapShopList(state.shopName, state.brandName, state.numProcess)
        .then((res) => {
            const { scrap_status, report_name } = res.data;
            scrap_status === "success" ? setReportName(report_name) : toast.error("에러 발생");
            enableButton();
        })
        .catch((e) => {
            console.log(e);
            toast.error("네트워크 에러 발생");
            enableButton();
        });
};
