"use client";

import { Table } from "@/app/production/product/component/table/table";

import { useEffect, useState } from "react";
import * as api from "./component/fetch";
import { CreateproductCardProps } from "@/app/types/type";
import CreateFormModal from "./component/modal/create-form-modal";
import { toast } from "react-toastify";

export default function Page() {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const [data, setData] = useState<CreateproductCardProps[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    const modalToggle = () => {
        setIsOpen(!isOpen);
    };

    useEffect(() => {
        api.getProduct().then((res) => {
            setData(res);
            setLoading(false);
        });
    }, []);

    const defaultData: CreateproductCardProps = {
        brand: "",
        productName: "",
        productId: "",
        price: "",
        shippingFee: "",
        intl: "",
        imgType: "",
        size: "",
        color: "",
        category: "",
    };

    return (
        <div className="py-12">
            <div className="flex-right">
                <div onClick={modalToggle} className="text-xl py-2 link-animation">
                    + 새로운 아이템 추가하기
                </div>
            </div>
            <Table defaultData={data} />
            <CreateFormModal defaultData={defaultData} isOpen={isOpen} setIsOpen={setIsOpen} />;
        </div>
    );
}
