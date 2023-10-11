"use client";

import CustomInput from "@/app/components/custom-input/cusotm-input";
import { useEffect, useState } from "react";
import * as api from "./fetch";
import { CreateproductCardProps } from "@/app/types/type";

export default function CreateForm({ openToggle }: { openToggle: () => void }) {
    const [brand, setBrand] = useState("");
    const [productName, setProductName] = useState("");
    const [productId, setProductId] = useState("");
    const [price, setPrice] = useState("");
    const [shippingFee, setShippingFee] = useState("");
    const [intl, setIntl] = useState("false");
    const [imgType, setImgType] = useState("");
    const [size, setSize] = useState("");
    const [color, setColor] = useState("");
    const [category, setCategory] = useState("");

    const data: CreateproductCardProps = {
        brand: brand,
        productName: productName,
        productId: productId,
        price: price,
        shippingFee: shippingFee,
        intl: intl,
        imgType: imgType,
        size: size,
        color: color,
        category: category,
    };

    if (process.env.NEXT_PUBLIC_IMAGE_TYPE === undefined) return <></>;
    if (process.env.NEXT_PUBLIC_BRAND === undefined) return <></>;
    if (process.env.NEXT_PUBLIC_CATEGORY === undefined) return <></>;
    const imgArray = process.env.NEXT_PUBLIC_IMAGE_TYPE;
    const brandArray = process.env.NEXT_PUBLIC_BRAND;
    const categoryArray = process.env.NEXT_PUBLIC_CATEGORY;

    return (
        <>
            <form action="" className="flex flex-col gap-8 ">
                <div className="flex gap-8">
                    <div>
                        <div className="flex-center">Brand</div>
                        <select
                            className="border border-black rounded-md px-4 py-2"
                            value={brand ? brand : "브랜드"}
                            onChange={(e) => setBrand(e.target.value)}>
                            {JSON.parse(brandArray).map((v: string, i: number) => (
                                <option value={v} key={i} selected={!i && true}>
                                    {v}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <div className="flex-center">Category</div>
                        <select
                            className="border border-black rounded-md px-4 py-2"
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}>
                            {JSON.parse(categoryArray).map((v: string, i: number) => (
                                <option value={v} key={i} selected={!i && true}>
                                    {v}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <div className="flex-center">Intl</div>
                        <select
                            className="border border-black rounded-md px-4 py-2"
                            value={intl}
                            onChange={(e) => setIntl(e.target.value)}>
                            <option value="true" selected={true}>
                                true
                            </option>
                            <option value="false">false</option>
                        </select>
                    </div>
                    <div>
                        <div className="flex-center">ImgType</div>
                        <select
                            className="border border-black rounded-md px-4 py-2"
                            value={imgType}
                            onChange={(e) => setImgType(e.target.value)}>
                            {JSON.parse(imgArray).map((v: string, i: number) => (
                                <option value={v} key={i} selected={!i && true}>
                                    {v}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
                <div className="grid grid-cols-2">
                    <CustomInput
                        label={"Product Name"}
                        value={productName}
                        setValue={setProductName}
                        id="productName"
                        info=""
                        checkPolicy={() => true}
                        type="text"
                    />
                    <CustomInput
                        label={"Product ID"}
                        value={productId}
                        setValue={setProductId}
                        id="productId"
                        info=""
                        checkPolicy={() => true}
                        type="text"
                    />
                    <CustomInput
                        label={"Price"}
                        value={price}
                        setValue={setPrice}
                        id="price"
                        info=""
                        checkPolicy={() => true}
                        type="text"
                    />
                    <CustomInput
                        label={"Shipping Fee"}
                        value={shippingFee}
                        setValue={setShippingFee}
                        id="shippingFee"
                        info=""
                        checkPolicy={() => true}
                        type="number"
                    />
                    <CustomInput
                        label={"Size"}
                        value={size}
                        setValue={setSize}
                        id="size"
                        info=""
                        checkPolicy={() => true}
                        type="text"
                    />
                    <CustomInput
                        label={"Color"}
                        value={color}
                        setValue={setColor}
                        id="color"
                        info=""
                        checkPolicy={() => true}
                        type="text"
                    />
                </div>
            </form>
            <div className="flex w-full gap-4 py-8">
                <button className="black-bar basis-3/4 " onClick={() => api.createProduct(data).then(openToggle)}>
                    등록하기
                </button>
                <button className="black-bar basis-1/4" onClick={openToggle}>
                    취소{" "}
                </button>
            </div>
        </>
    );
}
