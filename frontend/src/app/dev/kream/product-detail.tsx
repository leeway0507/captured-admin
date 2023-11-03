import { useReducer, useRef } from "react";
import { InitProductDetail } from "./fetch";

interface scrapingProps {
    brandName: string;
    numProcess: Number;
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
        if (state.numProcess === 0) {
            return alert("최대 스크롤 수를 입력해주세요");
        }

        const start = confirm(`브랜드네임 [${state.brandName}]이 맞으면 시작합니다.`);

        if (!start) {
            return;
        }

        disableButton();
        await InitProductDetail(state.brandName, state.numProcess, state.kreamIds)
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
                className="black-bar min-w-[150px] text-xl disabled:bg-rose-800 disabled:border disabled:border-main-black disabled:cursor-not-allowed disabled:text-white"
                onClick={() => handleSubmit(state)}>
                요청하기
            </button>
        </div>
    );
}