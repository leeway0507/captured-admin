"use client";
import { useRouter } from "next/navigation";
import React, { useReducer, useRef, useEffect, useState, ButtonHTMLAttributes } from "react";
import { ScrapShopPage, loadShopPageName, loadShopPageBrandName } from "./fetch-scrap";
import { toast } from "react-toastify";
import Select from "react-select";
import ShopBrandSelect from "./shop-brand-select";

const initialState = {
    searchType: "all",
    content: "1000",
    numProcess: 1,
};

export interface searchProps {
    searchType: string;
    content: string;
    numProcess: number;
}

export default function ShopCardPage() {
    const submitRef = useRef<HTMLButtonElement>(null);
    const [state, dispatch] = useReducer(reducer, initialState);
    const [scrapName, setScrapName] = useState("");

    const router = useRouter();

    useEffect(() => {
        if (scrapName === "") return;
        router.push(`/dev/shop/report/page/${scrapName}`);
    }, [scrapName, router]);

    const selectCat = [
        { value: "shopNameBrandName", label: "사이트명(브랜드)" },
        { value: "lastScrap", label: "최종수집 제품" },
        { value: "shopName", label: "사이트명" },
        { value: "productId", label: "제품 아이디" },
        { value: "shopProductCardId", label: "SKU" },
        { value: "brandName", label: "브랜드명" },
        { value: "all", label: "전체 수집" },
    ];

    return (
        <div className="flex pt-4 pb-24 gap-1 justify-between">
            <div className="flex gap-8 justify-space">
                <div className="min-w-[300px] flex flex-col">
                    <div className="text-xl">검색 타입 선정</div>
                    <Select
                        className="z-50"
                        defaultValue={selectCat[4]}
                        instanceId="searchType"
                        options={selectCat}
                        onChange={(e: any) => {
                            dispatch({ type: "searchType", payload: e.value });
                        }}
                    />
                </div>
                <div className="min-w-[150px] flex flex-col">
                    <InputList searchType={state.searchType} content={state.content} dispatch={dispatch} />
                </div>
            </div>
            <div className="min-w-[150px] flex flex-col">
                <label htmlFor="numProcess">프로세스 수 </label>
                <input
                    type="text"
                    name="numProcess"
                    id="numProcess"
                    onChange={(e) => {
                        dispatch({ type: "numProcess", payload: e.target.value });
                    }}
                    value={state.numProcess}
                    className="border border-main-black h-[50px] rounded-md px-4"
                />
            </div>
            <button
                ref={submitRef}
                className="black-bar-with-disabled min-w-[150px] text-xl "
                onClick={() => handleScrapProductPage(state, setScrapName, submitRef)}>
                요청하기
            </button>
        </div>
    );
}

const reducer = (state: searchProps, action: any) => {
    switch (action.type) {
        case "searchType":
            return { ...state, searchType: action.payload };
        case "content":
            return { ...state, content: action.payload };
        case "numProcess":
            return { ...state, numProcess: action.payload };
        default:
            return state;
    }
};

export const handleScrapProductPage = async (
    state: searchProps,
    setName: (scrapName: string) => void,
    ref: React.RefObject<HTMLButtonElement>
) => {
    const enableButton = () => {
        if (ref.current) {
            ref.current.disabled = false;
        }
    };

    const disableButton = () => {
        if (ref.current) {
            ref.current.disabled = true;
        }
    };
    if (state.searchType === "") {
        return toast.error("검색 타입을 선택하세요.");
    }
    if (state.content === "") {
        return toast.error("값을 입력하세요.");
    }

    const start = confirm(`수집을 시작합니다.`);

    if (!start) {
        return;
    }

    disableButton();
    await ScrapShopPage(state.searchType, state.content, state.numProcess)
        .then((res) => {
            const { scrap_status, report_name } = res.data;
            scrap_status === "success"
                ? (setName(report_name), enableButton())
                : (toast.error("에러 발생"), enableButton());
        })
        .catch((e) => {
            console.log(e);
            toast.error("네트워크 에러 발생");
            enableButton();
        });
};

const InputList = ({
    searchType,
    content,
    dispatch,
}: {
    searchType: string;
    content: string;
    dispatch: (e: any) => void;
}) => {
    const [shopSelect, setShopSelect] = useState("");
    const [brandSelect, setBrandSelect] = useState([""]);

    const Input = (
        <>
            <label htmlFor="content">값 입력</label>
            <input
                value={content}
                type="text"
                name="content"
                id="content"
                onChange={(e) => dispatch({ type: "content", payload: e.target.value })}
                className="border border-main-black h-[50px] rounded-md px-4"
            />
            <span className="text-xs">전체 수집 선택시 최대 수집 페이지 입력</span>
        </>
    );
    const storeSelect = (
        <>
            <div className="min-w-[300px] flex flex-row gap-2">
                <ShopBrandSelect
                    shopSelect={shopSelect}
                    setShopSelect={(e) => setShopSelect(e.value)}
                    brandSelect={brandSelect}
                    setBrandSelect={(e) => setBrandSelect(e)}
                />
            </div>
        </>
    );

    useEffect(() => {
        dispatch({ type: "content", payload: { shopName: shopSelect, brandName: brandSelect } });
    }, [dispatch, shopSelect, brandSelect]);

    return <>{searchType === "shopNameBrandName" ? storeSelect : Input}</>;
};
