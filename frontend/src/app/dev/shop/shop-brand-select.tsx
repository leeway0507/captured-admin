"use client";

import { useState, useEffect } from "react";
import { loadShopListBrandName, loadShopListName } from "./fetch-scrap";
import Select from "react-select";

export default function ShopBrandSelect({
    shopSelect,
    setShopSelect,
    brandSelect,
    setBrandSelect,
}: {
    shopSelect: string;
    setShopSelect: (v: any) => void;
    brandSelect: string[];
    setBrandSelect: (v: any) => void;
}) {
    const [shopList, setShopList] = useState([""]);
    const [brandList, setBrandList] = useState([""]);

    useEffect(() => {
        {
            loadShopListName().then((res) => {
                setShopList(res.data.map((option: string) => ({ value: option, label: option })));
            });
        }
    }, []);

    //load Brand Name
    useEffect(() => {
        if (shopSelect !== "")
            loadShopListBrandName(shopSelect).then((res) => {
                setBrandList(res.data.map((option: string) => ({ value: option, label: option })));
            });
    }, [shopSelect]);
    return (
        <>
            <div className="min-w-[300px] flex flex-col">
                <div>스크랩 샵 이름</div>
                <Select instanceId="shopName" options={shopList} onChange={setShopSelect} />
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
                        setBrandSelect(result);
                    }}
                />
                <div>{brandSelect}</div>
            </div>
        </>
    );
}
