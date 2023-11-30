"use client";
import { updateCandidate } from "../../../candidate-table/[...slug]/fetch";
import { getKreamColor, updateShopProductCard } from "../../fetch";
import { useState, useCallback } from "react";
import { toast } from "react-toastify";
import CreateFormModal from "@/app/production/product/component/modal/create-form-modal";
import SizeTableModal from "../modal/size-table-modal";
import { getSizeTableData } from "../../fetch";
import { productCardProps, sizeInfoprops } from "../modal/size-table-modal";

//css
export const candidateClass = "p-2 h-[150px] flex-center cursor-pointer";

export const updateToDB = (props: any) => {
    const { shopProductCardId, coupon, productId } = props.row.original;
    const value = {
        coupon: coupon,
        product_id: productId,
    };
    const handler = async () => {
        await updateShopProductCard(shopProductCardId, value).then((res) => {
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
    const { productId, shopName } = props.row.original;

    const [isOpen, setIsOpen] = useState(false);
    const [sizeInfo, setSizeInfo] = useState<sizeInfoprops[]>();
    const [productInfo, setProductInfo] = useState<productCardProps[]>();

    const openToggle = async () => {
        await getSizeTableData(productId).then((res) => {
            setSizeInfo(res.data.sizeInfo);
            setProductInfo(res.data.productInfo);
            res.data.sizeInfo.length === 0 ? toast.info("사이즈가 존재하지 않습니다.") : setIsOpen(true);
        });
    };

    return (
        <>
            <button className="bg-purple-600 text-white p-2 hover:bg-purple-500" onClick={openToggle}>
                사이즈
            </button>

            {sizeInfo && productInfo && (
                <SizeTableModal
                    initShopName={shopName}
                    sizeInfo={sizeInfo}
                    productInfo={productInfo}
                    isOpen={isOpen}
                    setIsOpen={setIsOpen}
                />
            )}
        </>
    );
};

export const SendDraft = (props: any) => {
    const sku = props.row.original.productInfo?.sku;
    const [isOpen, setIsOpen] = useState(false);

    const { brandName, shopProductName, productId } = props.row.original;
    const { sellPrice20P } = GetPrices(props);
    const shippingFee = 19000;
    const [defaultData, setDefaultData] = useState({
        brand: brandName,
        productName: shopProductName.replaceAll("-", " "),
        productId: productId,
        price: Math.round((sellPrice20P - shippingFee) / 1000) * 1000,
        shippingFee: shippingFee,
        intl: true,
        color: "",
        category: "",
        categorySpec: "",
        imgType: "",
    });
    const openToggle = () => {
        getKreamColor(productId).then((res) => {
            setIsOpen(true);
            setDefaultData((old) => ({ ...old, color: res.data.color ?? "/" }));
        });
    };

    console.log(isOpen);
    return sku === undefined ? (
        <>
            <button className="bg-blue-600 text-white p-2" onClick={openToggle}>
                초안작성
            </button>
            {defaultData.color && <CreateFormModal defaultData={defaultData} isOpen={isOpen} setIsOpen={setIsOpen} />}
        </>
    ) : (
        <div className="bg-green-600 text-white p-2">
            <div>배포 중</div>
            <div>sku:{sku}</div>
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

    const reverseStatus = status === "1" ? 2 : 1;

    event.target.dataset.status = reverseStatus;

    updateCandidate(id, reverseStatus).then((res) => {
        if (res.status === 200) {
            event.target.className =
                reverseStatus === 2 ? `bg-green-200 ${candidateClass}` : `bg-yellow-200 ${candidateClass}`;
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

    updateCandidate(id, reverseStatus).then((res) => {
        if (res.status === 200) {
            //remove candidate 상태 변경
            const removeClass = "flex-center h-[50px] mt-2";
            event.target.className =
                reverseStatus === 1 ? `bg-rose-200 ${removeClass}` : `bg-rose-600 text-white ${removeClass}`;
            event.target.dataset.status = reverseStatus;
            toast.success("업데이트 성공");
        }
    });
};
