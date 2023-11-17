"use client";

import { ProductInfoTable } from "./component/table/product-info-table";
import { useEffect, useState } from "react";
import * as api from "./component/fetch";
import { CreateproductCardProps } from "@/app/types/type";
import CreateFormModal from "./component/modal/create-form-modal";

export default function Page() {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const [data, setData] = useState<CreateproductCardProps[]>([]);

    const modalToggle = () => {
        setIsOpen(!isOpen);
    };

    useEffect(() => {
        api.getProduct().then((res) => {
            setData(res.data);
        });
    }, []);

    const defaultData: CreateproductCardProps = {
        brand: "",
        productName: "",
        productId: "",
        price: 0,
        shippingFee: 0,
        intl: true,
        imgType: "",
        color: "",
        category: "",
        categorySpec: "",
    };

    return (
        <div className="w-full">
            <div className="flex-right">
                <div onClick={modalToggle} className="text-xl link-animation">
                    + 새로운 아이템 추가하기
                </div>
            </div>
            <ProductInfoTable tableData={data} />
            <CreateFormModal defaultData={defaultData} isOpen={isOpen} setIsOpen={setIsOpen} />
        </div>
    );
}
