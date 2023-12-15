"use client";
import { useEffect, useReducer, useRef, useState } from "react";
import { InitProductDetail } from "./fetch";
import { useRouter } from "next/navigation";
import { toast, Flip } from "react-toastify";
export interface scrapingProps {
    brandName: string;
    numProcess: number;
    kreamIds: string;
}

const initialState = {
    brandName: "",
    numProcess: 1,
    kreamIds: "",
};

const reducer = (state: scrapingProps, action: any) => {
    switch (action.type) {
        case "brandName":
            return { ...state, brandName: action.payload };
        case "numProcess":
            return { ...state, numProcess: action.payload };
        case "kreamIds":
            return { ...state, kreamIds: action.payload };

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
    if (state.brandName === "") {
        return toast.error("브랜드 네임을 입력해주세요.");
    }
    if (state.numProcess === 0) {
        return toast.error("최대 스크롤 수를 입력해주세요.");
    }

    const start = confirm(`브랜드네임 [${state.brandName}]이 맞으면 시작합니다.`);

    if (!start) {
        return;
    }

    disableButton();
    await InitProductDetail(state.brandName, state.numProcess, state.kreamIds)
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

export default function PrdoucCardList() {
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
        router.push(`/dev/kream/scrap-result/${scrapName}`);
    }, [scrapName, router]);

    return (
        <div className="flex gap-8 justify-between">
            <div className="min-w-[200px] flex flex-col">
                <label htmlFor="brandName">브랜드 네임</label>
                <input
                    type="text"
                    name="brandName"
                    id="brandName"
                    onChange={(e) => {
                        dispatch({ type: "brandName", payload: e.target.value });
                    }}
                    value={state.brandName}
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
            <div className="min-w-[200px] flex flex-col">
                <label htmlFor="kreamIds">크림 id(띄어쓰기 없이 ,로 구분)</label>
                <input
                    type="text"
                    name="kreamIds"
                    id="kreamIds"
                    onChange={(e) => {
                        dispatch({ type: "kreamIds", payload: e.target.value });
                    }}
                    value={state.kreamIds}
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
