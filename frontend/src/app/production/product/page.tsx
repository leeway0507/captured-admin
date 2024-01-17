"use client";

import { ProductInfoTable } from "./component/table/product-info-table";
import { useEffect, useState } from "react";
import { CreateproductCardProps } from "@/app/types/type";
import RegisterProductFormModal from "./component/modal/register-product-form-modal";

export default function Page() {
    const [isOpen, setIsOpen] = useState<boolean>(false);

    const modalToggle = () => {
        setIsOpen(!isOpen);
    };

    const defaultData: CreateproductCardProps = {
        brand: "",
        korBrand: "",
        productName: "",
        korProductName: "",
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
            <ProductInfoTable />
            <RegisterProductFormModal defaultData={defaultData} isOpen={isOpen} setIsOpen={setIsOpen} />
        </div>
    );
}
