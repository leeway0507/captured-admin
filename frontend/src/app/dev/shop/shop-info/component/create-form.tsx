"use client";

import CustomInput from "@/app/production/prod-components/custom-input/cusotm-input";
import { useEffect, useState, useReducer } from "react";
import * as api from "./fetch";
import { shopInfoProps } from "../../type";
import { toast } from "react-toastify";

const initialState: shopInfoProps = {
    shopName: "",
    shopUrl: "",
    taxReductionRate: 0,
    delAgcTaxReductionRate: 0,
    domeShipPrice: 0,
    intlShipPrice: 0,
    fromUsShipping: false,
    isDdp: false,
    country: "",
};

const reducer = (state: shopInfoProps, action: any) => {
    switch (action.type) {
        case "shopName":
            return { ...state, shopName: action.payload };
        case "shopUrl":
            return { ...state, shopUrl: action.payload };
        case "taxReductionRate":
            return { ...state, taxReductionRate: action.payload };
        case "delAgcTaxReductionRate":
            return { ...state, delAgcTaxReductionRate: action.payload };
        case "domeShipPrice":
            return { ...state, domeShipPrice: action.payload };
        case "intlShipPrice":
            return { ...state, intlShipPrice: action.payload };
        case "fromUsShipping":
            return { ...state, fromUsShipping: action.payload };
        case "isDdp":
            return { ...state, isDdp: action.payload };
        case "country":
            return { ...state, country: action.payload };

        default:
            return state;
    }
};

export default function CreateForm({ openToggle }: { openToggle: () => void }) {
    const [state, dispatch] = useReducer(reducer, initialState);

    return (
        <>
            <form action="" className="flex flex-col gap-8 ">
                <div className="grid grid-cols-2 gap-12">
                    <CustomInput
                        label={"스토어이름"}
                        value={state.shopName}
                        setValue={(e) => dispatch({ type: "shopName", payload: e })}
                        id="shopName"
                        info=""
                        checkPolicy={() => true}
                        type="text"
                    />
                    <CustomInput
                        label={"shopUrl"}
                        value={state.shopUrl}
                        setValue={(e) => dispatch({ type: "shopUrl", payload: e })}
                        id="shopUrl"
                        info=""
                        checkPolicy={() => true}
                        type="text"
                    />
                    <CustomInput
                        label={"부가세 감면율"}
                        value={state.taxReductionRate}
                        setValue={(e) => dispatch({ type: "taxReductionRate", payload: e })}
                        id="taxReductionRate"
                        info=""
                        checkPolicy={() => true}
                        type="number"
                    />
                    <CustomInput
                        label={"배대지 부가세 감면율"}
                        value={state.delAgcTaxReductionRate}
                        setValue={(e) => dispatch({ type: "delAgcTaxReductionRate", payload: e })}
                        id="delAgcTaxReductionRate"
                        info=""
                        checkPolicy={() => true}
                        type="number"
                    />
                    <CustomInput
                        label={"배대지 배송비"}
                        value={state.domeShipPrice}
                        setValue={(e) => dispatch({ type: "domeShipPrice", payload: e })}
                        id="domeShipPrice"
                        info=""
                        checkPolicy={() => true}
                        type="number"
                    />
                    <CustomInput
                        label={"국제 배송비"}
                        value={state.intlShipPrice}
                        setValue={(e) => dispatch({ type: "intlShipPrice", payload: e })}
                        id="intlShipPrice"
                        info=""
                        checkPolicy={() => true}
                        type="number"
                    />
                </div>
                <div className="flex gap-8">
                    <CustomInput
                        label={"스토어 국가"}
                        value={state.country}
                        setValue={(e) => dispatch({ type: "country", payload: e })}
                        id="country"
                        info=""
                        checkPolicy={() => true}
                        type="text"
                    />
                    <div>
                        <div className="flex-center">fromUsShipping</div>
                        <select
                            className="border border-black rounded-md px-4 py-2"
                            value={state.fromUsShipping}
                            onChange={(e) => dispatch({ type: "fromUsShipping", payload: e.target.value })}>
                            <option value="true" selected={true}>
                                true
                            </option>
                            <option value="false">false</option>
                        </select>
                    </div>
                    <div>
                        <div className="flex-center">isDdp</div>
                        <select
                            className="border border-black rounded-md px-4 py-2"
                            value={state.isDdp}
                            onChange={(e) => dispatch({ type: "isDdp", payload: e.target.value })}>
                            <option value="true" selected={true}>
                                true
                            </option>
                            <option value="false">false</option>
                        </select>
                    </div>
                </div>
            </form>
            <div className="flex w-full gap-4 py-8">
                <button
                    className="black-bar basis-3/4 "
                    onClick={() =>
                        api
                            .createShopInfo(state)
                            .then((res) => {
                                res.status === 200
                                    ? (toast.success("요청 성공"), openToggle())
                                    : toast.error(`에러 발생 :${res.status}`);
                            })
                            .catch((err) => {
                                toast.error(`에러 발생 :${err}`);
                            })
                    }>
                    등록하기
                </button>
                <button className="black-bar basis-1/4" onClick={openToggle}>
                    취소{" "}
                </button>
            </div>
        </>
    );
}
