"use client";

import { ShopInfoTable } from "./component/table/shop-info-table";
import CreateForm from "./component/create-form";
import { useEffect, useState } from "react";
import * as api from "./component/fetch";
import { shopInfoProps } from "../type";

export default function Page() {
    const [open, setOpen] = useState<Boolean>(false);
    const [data, setData] = useState<shopInfoProps[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    const openToggle = () => {
        setOpen(!open);
    };

    useEffect(() => {
        api.getShopInfo().then((res) => {
            setData(res.data);
            setLoading(false);
        });
    }, []);

    if (loading) return <></>;

    console.log(data);

    return (
        <div className="py-12">
            <div className="flex-left relative">
                <button type="button" onClick={openToggle} className=" text-xl py-2 link-animation">
                    + 새로운 아이템 추가하기
                </button>
                <div className={`absolute top-full max-w-[1440px] bg-white z-50 w-full  ${open ? "block" : "hidden"} `}>
                    <div className="rounded-lg border-2 p-16 ">
                        <CreateForm openToggle={openToggle} />
                    </div>
                </div>
            </div>
            <ShopInfoTable tableData={data} />
        </div>
    );
}
