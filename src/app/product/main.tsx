"use client";
import { Table } from "@/app/components/table/table";
import CreateForm from "./component/create-form";
import { useEffect, useState } from "react";
import { getProduct } from "./component/fetch";
import { CreateproductCardProps } from "@/app/types/type";

export default function Main() {
    const [open, setOpen] = useState<Boolean>(false);
    const [data, setData] = useState<CreateproductCardProps[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    const openToggle = () => {
        setOpen(!open);
    };

    useEffect(() => {
        getProduct().then((res) => {
            setData(res), console.log(res);
            setLoading(false);
        });
    }, []);

    if (loading) return <></>;

    return (
        <div className="py-12">
            <div className="flex-right relative">
                <button type="button" onClick={openToggle} className=" text-xl py-2 link-animation">
                    + 새로운 아이템 추가하기
                </button>
                <div className={`absolute top-full max-w-[1440px] bg-white z-50 w-full  ${open ? "block" : "hidden"} `}>
                    <div className="rounded-lg border-2 p-16 ">
                        <CreateForm openToggle={openToggle} />
                    </div>
                </div>
            </div>
            <Table defaultData={data} />
        </div>
    );
}
