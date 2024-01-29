"use client";
import { deleteCandidateCard, patchCandidateCard, updateCandidateCard, getSizeData } from "../fetch";
import { getKreamData } from "../fetch";
import { useState, useCallback } from "react";
import { toast } from "react-toastify";
import RegisterProductFormModal from "@/app/production/product/component/modal/register-product-form-modal";
import SizeTableModal from "../modal/size-table-modal";
import { sizeProps } from "../modal/size-table-modal";

//css
export const candidateClass = "p-2 h-[150px] flex-center cursor-pointer";

export const updateToDB = (props: any) => {
    const { shopProductCardId, coupon, productId } = props.row.original;
    const value = { coupon, productId };
    const handler = async () => {
        await updateCandidateCard(shopProductCardId, value).then((res) => {
            res.status === 200 ? toast.success("업데이트 성공") : toast.error("업데이트 실패");
        });
    };
    return (
        <button onClick={handler} className="bg-main-black text-white p-2 active:bg-blue-black">
            DB 저장
        </button>
    );
};

export const GetSizeTable = (props: any) => {
    const { shopProductCardId, shopName } = props.row.original;
    const [isOpen, setIsOpen] = useState(false);
    const [size, setSize] = useState<sizeProps>();
    const openToggle = async () => {
        await getSizeData(shopProductCardId).then((res) => {
            setSize(res.data);
            res.data.meta.shop.length === 0 ? toast.info("사이즈가 존재하지 않습니다.") : setIsOpen(true);
        });
    };

    return (
        <>
            <button onClick={openToggle} className="bg-purple-600 text-white p-2 hover:bg-purple-500">
                사이즈
            </button>

            {size && (
                <SizeTableModal initShopName={shopName ?? "all"} size={size} isOpen={isOpen} setIsOpen={setIsOpen} />
            )}
        </>
    );
};

export const SendDraft = (props: any) => {
    const sku = props.row.original.productInfo?.sku;

    const [isOpen, setIsOpen] = useState(false);

    const { brandName, shopProductName, productId, korBrand, korProductName } = props.row.original;
    const { sellPrice20P, sellPrice10P } = GetPrices(props);
    const shippingFee = 15000;
    const avgRetailPrice = Math.round((sellPrice10P + sellPrice20P) / 2);
    const [defaultData, setDefaultData] = useState({
        brand: brandName,
        korBrand: korBrand,
        korProductName: korProductName,
        productName: shopProductName.replaceAll("-", " "),
        productId: productId,
        price: Math.round((avgRetailPrice - shippingFee) / 1000) * 1000,
        shippingFee: shippingFee,
        intl: true,
        color: "",
        category: "",
        categorySpec: "",
        imgType: "webp",
    });

    const openToggle = () => {
        getKreamData(productId).then((res) => {
            setIsOpen(true);
            setDefaultData((old) => ({ ...old, color: res.data[0]?.color ?? "/" }));
        });
    };

    return sku === undefined ? (
        <>
            <button className="bg-blue-600 text-white p-2" onClick={openToggle}>
                초안작성
            </button>
            {defaultData.color && (
                <RegisterProductFormModal defaultData={defaultData} isOpen={isOpen} setIsOpen={setIsOpen} />
            )}
        </>
    ) : (
        <div className="bg-green-600 text-white p-2 text-sm">
            <div>SKU:{sku}</div>
        </div>
    );
};

interface Prices {
    korPrice: number;
    usPrice: number;
    PriceWithCoupon: number;
    taxReductionOriginalPrice: number;
    intlShipKorPrice: number;
    customFee: number;
    VATFee: number;
    totalPriceBeforeCardFee: number;
    sellPrice10P: number;
    sellPrice20P: number;
    cardFee: number;
}

function calcCustomAndVAT(
    usPrice: number,
    korPrice: number,
    intlShipKorPrice: number,
    customRate: number,
    VATRate: number,
    isDdp: boolean,
    fromUsShipping: boolean
) {
    if (usPrice < 150) return [0, 0];
    if (usPrice < 200 && fromUsShipping) return [0, 0];
    if (isDdp) return [0, 0];

    const customFee = (korPrice + intlShipKorPrice) * customRate;
    const VATFee = (korPrice + intlShipKorPrice + customFee) * VATRate;
    return [customFee, VATFee];
}

export function GetPrices(props: any): Prices {
    const calculatePrices = useCallback(() => {
        const { originalPrice, buyingCurrency, usCurrency, errorRate, coupon } = props.row.original;
        const { taxReductionRate } = props.row.original.shopInfo;

        const { intlShipPrice } = props.row.original.shopInfo;

        const currencyRate = buyingCurrency * errorRate;
        const taxReductionOriginalPrice = originalPrice / (1 + taxReductionRate);

        const PriceWithCoupon =
            coupon > 0 ? taxReductionOriginalPrice / (1 + Number(coupon)) : taxReductionOriginalPrice;
        const korPrice = PriceWithCoupon * currencyRate;

        const usPrice = korPrice / usCurrency;

        const intlShipKorPrice = Math.round(intlShipPrice * currencyRate);
        const [d1, d2] = calcCustomAndVAT(
            usPrice,
            korPrice,
            intlShipKorPrice,
            props.row.original.customRate,
            props.row.original.VATRate,
            props.row.original.shopInfo.isDdp,
            props.row.original.shopInfo.fromUsShipping
        );
        const customFee = Math.round(d1);
        const VATFee = Math.round(d2);

        const totalPriceBeforeCardFee = korPrice + intlShipKorPrice + customFee + VATFee;

        const sellPrice10P = Math.round((totalPriceBeforeCardFee * 100) / 87);
        const sellPrice20P = Math.round((totalPriceBeforeCardFee * 100) / 77);

        const cardFee = Math.round(sellPrice20P * props.row.original.cardRate);

        return {
            korPrice,
            usPrice,
            PriceWithCoupon,
            taxReductionOriginalPrice,
            intlShipKorPrice,
            customFee,
            VATFee,
            totalPriceBeforeCardFee,
            sellPrice10P,
            sellPrice20P,
            cardFee,
        };
    }, [props.row.original]);

    return calculatePrices();
}

export const handleCandidate = (event: any) => {
    const { id, status } = event.target.dataset;

    const changeStatus = () => {
        switch (status) {
            case "0":
                return 2;
            case "1":
                return 0;
            case "2":
                return 1;
            default:
                return 0;
        }
    };
    const reverseStatus = changeStatus();

    event.target.dataset.status = reverseStatus;

    patchCandidateCard(id, "candidate", reverseStatus).then((res) => {
        if (res.status === 200) {
            event.target.className =
                reverseStatus === 0
                    ? `bg-red-200 ${candidateClass}`
                    : reverseStatus === 1
                    ? `bg-yellow-200 ${candidateClass}`
                    : `bg-green-200 ${candidateClass}`;
            event.target.dataset.status = reverseStatus;
            toast.success("업데이트 성공");
        }
    });
};

export const handleRemoveCandidate = (event: any) => {
    const { id, status: removeStatus } = event.target.dataset;

    const mainStatus = document.getElementById(`status-${id}`)?.dataset.status;
    if (mainStatus === "2") return toast.error("수집 제품이므로 해제 불가합니다.");

    const reverseStatus = removeStatus === "1" ? 0 : 1;

    deleteCandidateCard(id).then((res) => {
        if (res.status === 200) {
            //remove candidate 상태 변경
            const removeClass = "flex-center h-[100px] mt-2";
            event.target.className =
                reverseStatus === 1 ? `bg-orange-200 ${removeClass}` : `bg-orange-400 text-white ${removeClass}`;
            event.target.dataset.status = reverseStatus;
            toast.success(`후보 제거 완료 : ${id}`, { autoClose: 500 });
        }
    });
};
