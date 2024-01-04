"use client";
import BaseModal from "./base-modal";
import { CreateproductCardProps } from "@/app/types/type";
import { useEffect, useReducer } from "react";
import CustomInput from "@/app/production/prod-components/custom-input/cusotm-input";
import { createProduct } from "../fetch";
import { toast } from "react-toastify";
import Select from "react-select";
import envJson from "@/app/env.json";

type CategorySpec = {
    의류: string[];
    신발: string[];
    기타: string[];
    [key: string]: string[]; // Index signature
};

const reducer = (state: CreateproductCardProps, action: { type: string; payload: any }) => {
    switch (action.type) {
        case "brand":
            return { ...state, brand: action.payload };
        case "productName":
            return { ...state, productName: action.payload };
        case "productId":
            return { ...state, productId: action.payload };
        case "price":
            return { ...state, price: action.payload };
        case "shippingFee":
            return { ...state, shippingFee: action.payload };
        case "intl":
            return { ...state, intl: action.payload };
        case "imgType":
            return { ...state, imgType: action.payload };
        case "color":
            return { ...state, color: action.payload };
        case "category":
            return { ...state, category: action.payload };
        case "categorySpec":
            return { ...state, categorySpec: action.payload };
        default:
            return state;
    }
};

const RegisterProductFormModal = ({
    defaultData,
    isOpen,
    setIsOpen,
}: {
    defaultData: CreateproductCardProps;
    isOpen: boolean;
    setIsOpen: (v: boolean) => void;
}) => {
    const [state, dispatch] = useReducer(reducer, defaultData);
    const closeModal = () => setIsOpen(false);

    const imgArray = envJson.NEXT_PUBLIC_IMAGE_TYPE;
    const brandArray = envJson.NEXT_PUBLIC_BRAND_ARRAY;
    const categoryArray = envJson.NEXT_PUBLIC_CATEGORY;
    const categorySpecObject: CategorySpec = envJson.NEXT_PUBLIC_CATEGORY_SPEC;

    const imgType = imgArray.map((v: string) => ({ value: v, label: v }));
    const category = categoryArray.map((v: string) => ({ value: v, label: v }));

    const initCat = state.category === "" ? category[0].value : (state.category as string);
    const categorySpec = categorySpecObject[initCat].map((v: string) => ({
        value: v,
        label: v,
    }));

    const intl = [
        { value: true, label: "해외배송" },
        { value: false, label: "국내배송" },
    ];

    useEffect(() => {
        const CalcshippingFee = (category: string) => (category === "신발" ? 19000 : 15000);
        dispatch({ type: "shippingFee", payload: CalcshippingFee(state.category) });
    }, [state.category]);

    const registrationHandler = async (state: CreateproductCardProps) => {
        const isValid = Object.values(state).every((value) => value !== "");

        if (!isValid)
            return Object.entries(state).forEach((v) => {
                if (v[1] === "") return toast.error(`${v[0]}이 비어있습니다.}`);
            });

        return await createProduct(state).then((res) =>
            res.status === 200
                ? (closeModal(), toast.success(`제품 등록에 성공했습니다. sku : ${res.data.sku}`, { autoClose: 5000 }))
                : toast.error("제품 등록에 실패했습니다.")
        );
    };

    const content = (
        <div className="p-2 max-w-3xl m-auto flex flex-col">
            <form action="" className="flex flex-col gap-8 ">
                <div className="flex  w-full justify-between">
                    <Select
                        defaultValue={brandArray.find((v) => v.value === state.brand)}
                        className="w-1/4"
                        instanceId="brandArray"
                        options={brandArray}
                        onChange={(e: any) => {
                            dispatch({ type: "brand", payload: e.label });
                        }}
                    />
                    <Select
                        defaultValue={imgType[1]}
                        instanceId="imgType"
                        options={imgType}
                        onChange={(e: any) => {
                            dispatch({ type: "imgType", payload: e.value });
                        }}
                    />
                    <Select
                        instanceId="category"
                        options={category}
                        onChange={(e: any) => {
                            dispatch({ type: "category", payload: e.value });
                        }}
                    />
                    <Select
                        instanceId="categorySpec"
                        className="w-1/5"
                        options={categorySpec}
                        onChange={(e: any) => {
                            dispatch({ type: "categorySpec", payload: e.value });
                        }}
                    />
                    <Select
                        defaultValue={intl[0]}
                        instanceId="intl"
                        options={intl}
                        onChange={(e: any) => {
                            dispatch({ type: "intl", payload: e.value });
                        }}
                    />
                </div>
                <div className="grid grid-cols-2 gap-8">
                    <div className="col-span-2">
                        <CustomInput
                            label={"Product Name"}
                            value={state.productName}
                            setValue={(e) => dispatch({ type: "productName", payload: e })}
                            id="productName"
                            info=""
                            checkPolicy={() => true}
                            type="text"
                        />
                    </div>
                    <CustomInput
                        label={"Product ID"}
                        value={state.productId}
                        setValue={(e) => dispatch({ type: "productId", payload: e })}
                        id="productId"
                        info=""
                        checkPolicy={() => true}
                        type="text"
                    />
                    <CustomInput
                        label={"Price"}
                        value={state.price}
                        setValue={(e) => dispatch({ type: "price", payload: e })}
                        id="price"
                        info=""
                        checkPolicy={() => true}
                        type="text"
                    />
                    <CustomInput
                        label={"Shipping Fee"}
                        value={state.shippingFee}
                        setValue={(e) => dispatch({ type: "shippingFee", payload: e })}
                        id="shippingFee"
                        info=""
                        checkPolicy={() => true}
                        type="number"
                    />
                    <CustomInput
                        label={"Color"}
                        value={state.color}
                        setValue={(e) => dispatch({ type: "color", payload: e })}
                        id="color"
                        info=""
                        checkPolicy={() => true}
                        type="text"
                    />
                </div>
            </form>
            <div className="flex-center w-full gap-4 py-8">
                <button className="black-bar-xl basis-2/4 " onClick={() => registrationHandler(state)}>
                    등록하기
                </button>
                <button className="black-bar-xl basis-1/4" onClick={closeModal}>
                    취소{" "}
                </button>
            </div>
        </div>
    );

    if (envJson.NEXT_PUBLIC_IMAGE_TYPE === undefined) return toast.info("IMAGE_TYPE이 정의되지 않았습니다.");
    if (envJson.NEXT_PUBLIC_BRAND_ARRAY === undefined) return toast.info("BRAND_ARRAY이 정의되지 않았습니다.");
    if (envJson.NEXT_PUBLIC_CATEGORY === undefined) return toast.info("CATEGORY가 정의되지 않았습니다.");

    return BaseModal({
        content: content,
        isOpen: isOpen,
        closeModal: closeModal,
    });
};

export default RegisterProductFormModal;
