"use client";
import { useEffect, useReducer, useRef, useState } from "react";
import { InitProductPage } from "./fetch";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";
import Select from "react-select";
export interface scrapingProps {
    searchType: string;
    searchValue: string;
    numProcess: number;
}

const initialState = {
    searchType: "lastScrap",
    searchValue: "",
    numProcess: 1,
};

const searchTypeOptions = [
    { value: "lastScrap", label: "최신 수집" },
    { value: "sku", label: "SKU" },
    { value: "product_id", label: "제품 아이디" },
];

const reducer = (state: scrapingProps, action: any) => {
    switch (action.type) {
        case "searchValue":
            return { ...state, searchValue: action.payload };
        case "numProcess":
            return { ...state, numProcess: action.payload };
        case "searchType":
            return { ...state, searchType: action.payload };

        default:
            return state;
    }
};

export const handleProductDtailSubmit = async (
    state: scrapingProps,
    setName: (scrapName: string) => void,
    enableButton: () => void,
    disableButton: () => void
) => {
    if (state.searchValue === "") {
        return toast.error("값을 입력해주세요.");
    }
    if (state.numProcess === 0) {
        return toast.error("최대 스크롤 수를 입력해주세요.");
    }

    const start = confirm(`요청 값 [${state.searchValue.slice(0, 10)}....]이 맞으면 시작합니다.`);

    if (!start) {
        return;
    }

    disableButton();

    await InitProductPage(state.searchType, state.searchValue, state.numProcess)
        .then((res) => {
            const { scrap_status, ...restData } = res.data;
            scrap_status === "success" ? setName(restData.scrap_name) : toast.error("에러 발생");
            enableButton();
        })
        .catch((e) => {
            toast.error("네트워크 에러 발생");
            enableButton();
        });
};

export default function PlatformPage() {
    const router = useRouter();
    const submitRef = useRef<HTMLButtonElement>(null);
    const [state, dispatch] = useReducer(reducer, initialState);
    const [scrapName, setScrapName] = useState("");

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

    useEffect(() => {
        if (scrapName === "") return;
        router.push(`/dev/kream/scrap-result/page/${scrapName}-kream`);
    }, [scrapName, router]);

    return (
        <div className="flex gap-8 justify-between">
            <Select
                options={searchTypeOptions}
                defaultValue={searchTypeOptions[0]}
                onChange={(opt) => dispatch({ type: "searchType", payload: opt?.value })}
                className="min-w-[200px] max-w-full mt-auto"
            />

            <div className="min-w-[200px] flex flex-col">
                <label htmlFor="searchValue">수집 값</label>
                <input
                    type="text"
                    name="searchValue"
                    id="searchValue"
                    onChange={(e) => {
                        dispatch({ type: "searchValue", payload: e.target.value });
                    }}
                    value={state.searchValue}
                    className="border border-main-black h-[50px] rounded-md px-4"
                />
            </div>
            <div className="min-w-[150px] flex flex-col">
                <label htmlFor="numProcess">프로세스 수 </label>
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
                className="black-bar-with-disabled min-w-[150px] text-xl"
                onClick={() => handleProductDtailSubmit(state, setScrapName, enableButton, disableButton)}>
                요청하기
            </button>
        </div>
    );
}
