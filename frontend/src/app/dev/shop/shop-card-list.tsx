"use client";
import { useRouter } from "next/navigation";
import { useReducer, useRef, useEffect, useState } from "react";
import { InitshopCardList, loadShopName, loadBrandName } from "./fetch";
import { toast } from "react-toastify";
import Select from "react-select";

interface scrapingProps {
    shopName: string;
    brandName: string;
    numProcess: number;
}

const initialState = {
    shopName: "",
    brandName: "",
    numProcess: 1,
};

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
    setName: (scrapName: string) => void,
    enableButton: () => void,
    disableButton: () => void
) => {
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
    await InitshopCardList(state.shopName, state.brandName, state.numProcess)
        .then((res) => {
            const { scrap_status, ...restData } = res.data;
            scrap_status === "success" ? setName(restData.scrap_name) : toast.error("에러 발생");
            enableButton();
        })
        .catch((e) => {
            console.log(e);
            toast.error("네트워크 에러 발생");
            enableButton();
        });
};

export default function ShopCardList() {
    const submitRef = useRef<HTMLButtonElement>(null);
    const [state, dispatch] = useReducer(reducer, initialState);
    const [shopList, setShopList] = useState([]);
    const [brandList, setBrandList] = useState([]);
    const [scrapName, setScrapName] = useState("");

    const router = useRouter();

    useEffect(() => {
        loadShopName().then((res) => {
            setShopList(res.data.map((option: string) => ({ value: option, label: option })));
        });
    }, []);

    useEffect(() => {
        if (state.shopName !== "")
            loadBrandName(state.shopName).then((res) => {
                setBrandList(res.data.map((option: string) => ({ value: option, label: option })));
            });
    }, [state.shopName]);

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
        router.push(`/dev/shop/scrap-result/list/${scrapName}-${state.shopName}`);
    }, [scrapName, router, state.shopName]);

    return (
        <div className="flex pt-4 pb-24 gap-1 justify-between max-w-5xl">
            <div className="min-w-[300px] flex flex-col">
                <div>스크랩 샵 이름</div>
                <Select
                    instanceId="shopName"
                    options={shopList}
                    onChange={(e: any) => {
                        dispatch({ type: "shopName", payload: e.value });
                    }}
                />
            </div>
            <div className="w-[300px] flex flex-col">
                <div>브랜드 이름</div>
                <Select
                    closeMenuOnSelect={false}
                    instanceId="brandName"
                    options={brandList}
                    isMulti
                    onChange={(e: any) => {
                        const result = e.reduce(
                            (accumulator: string, currentValue: { value: string; label: string }, index: number) => {
                                const separator = index === e.length - 1 ? "" : ",";
                                return accumulator + currentValue.value + separator;
                            },
                            ""
                        );
                        dispatch({ type: "brandName", payload: result });
                    }}
                />
                <div>{state.brandName}</div>
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
                className="black-bar-with-disabled min-w-[150px] text-xl h-[100px] "
                onClick={() => handleSubmit(state, setScrapName, enableButton, disableButton)}>
                요청하기
            </button>
        </div>
    );
}
