import { useReducer, useRef } from "react";
import { InitProductCardList } from "./fetch";

interface scrapingProps {
    brandName: string;
    maxScroll: Number;
    minWish: Number;
    minVolume: Number;
}

const initialState = {
    brandName: "",
    maxScroll: 20,
    minWish: 100,
    minVolume: 100,
};

const reducer = (state: scrapingProps, action: any) => {
    switch (action.type) {
        case "brandName":
            return { ...state, brandName: action.payload };
        case "maxScroll":
            return { ...state, maxScroll: action.payload };
        case "minWish":
            return { ...state, minWish: action.payload };
        case "minVolume":
            return { ...state, minVolume: action.payload };
        default:
            return state;
    }
};

export default function PrdoucCardList() {
    const submitRef = useRef<HTMLButtonElement>(null);
    const [state, dispatch] = useReducer(reducer, initialState);

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

    const handleSubmit = async (state: scrapingProps) => {
        if (state.brandName === "") {
            return alert("브랜드 네임을 입력해주세요");
        }
        if (state.maxScroll === 0) {
            return alert("최대 스크롤 수를 입력해주세요");
        }

        const start = confirm(`브랜드네임 [${state.brandName}]이 맞으면 시작합니다.`);

        if (!start) {
            return;
        }

        disableButton();
        await InitProductCardList(state.brandName, state.maxScroll, state.minWish, state.minVolume)
            .then((res) => {
                res.status === 200 ? alert("요청 완료") : alert(`에러 발생 :${res.status}`);
                enableButton();
            })
            .catch((e) => {
                console.log(e);
                alert("네트워크 에러 발생");
                enableButton();
            });
    };
    return (
        <div className="flex pt-4 pb-24 gap-8 justify-between">
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
                <label htmlFor="maxScroll">최대 스크롤 수 </label>
                <input
                    type="text"
                    name="maxScroll"
                    id="maxScroll"
                    onChange={(e) => {
                        e.target.value;
                        dispatch({ type: "maxScroll", payload: e.target.value });
                    }}
                    value={state.maxScroll}
                    className="border border-main-black h-[50px] rounded-md px-4"
                />
            </div>
            <div className="min-w-[150px] flex flex-col">
                <label htmlFor="minWish">최소 찜 수</label>
                <input
                    type="text"
                    name="minWish"
                    id="minWish"
                    onChange={(e) => {
                        dispatch({ type: "minWish", payload: e.target.value });
                    }}
                    value={state.minWish}
                    className="border border-main-black h-[50px] rounded-md px-4"
                />
            </div>
            <div className="w-[150px] flex flex-col">
                <label htmlFor="minVolume">최소 거래량</label>
                <input
                    type="text"
                    name="minVolume"
                    id="minVolume"
                    onChange={(e) => {
                        dispatch({ type: "minVolume", payload: e.target.value });
                    }}
                    value={state.minVolume}
                    className="border border-main-black h-[50px] rounded-md px-4"
                />
            </div>
            <button
                ref={submitRef}
                className="black-bar min-w-[150px] text-xl disabled:bg-rose-800 disabled:border disabled:border-main-black disabled:cursor-not-allowed disabled:text-white"
                onClick={() => handleSubmit(state)}>
                요청하기
            </button>
        </div>
    );
}
