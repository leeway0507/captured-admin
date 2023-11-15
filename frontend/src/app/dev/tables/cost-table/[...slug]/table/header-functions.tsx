"use client";
import KreamProductModal from "../../../kream-table/[...slug]/modal/kream-product-modal";
import { updateCandidate } from "../../../candidate-table/[...slug]/fetch";
import { updateChangesToDB } from "../../fetch";
import { useState, useCallback } from "react";
import { toast } from "react-toastify";

//css
export const candidateClass = "p-2 h-[150px] flex-center cursor-pointer";

interface optionProps {
    label: string;
    value: string;
}

export const OpenDetail = (props: any) => {
    const { productId, totalPriceBeforeCardFee } = props.row.original;
    const [isOpen, setIsOpen] = useState(false);

    const cost = totalPriceBeforeCardFee * 1.05 + 3000;

    return (
        <>
            <button
                className="bg-gray-200 hover:bg-gray-300 p-2 whitespace-nowrap"
                onClick={() => {
                    setIsOpen(true);
                }}>
                크림정보
            </button>
            {isOpen && (
                <KreamProductModal
                    searchType="productId"
                    value={productId}
                    isOpen={isOpen}
                    setIsOpen={setIsOpen}
                    cost={Math.round(cost)}
                />
            )}
        </>
    );
};

export const EditCell = (props: any) => {
    const { row, table } = props;

    const meta = table.options.meta;
    const setEditedRows = (e: React.MouseEvent<HTMLButtonElement>) => {
        const elName = e.currentTarget.name;
        meta?.setEditedRows((old: []) => ({
            ...old,
            [row.id]: !old[row.id],
        }));
        if (elName !== "edit") {
            meta?.revertData(row.index, e.currentTarget.name === "cancel");
        }
    };
    return (
        <div className="edit-cell-container w-[50px] flex-center">
            {meta?.editedRows[row.id] ? (
                <div className="edit-cell">
                    <button onClick={setEditedRows} name="cancel">
                        X
                    </button>
                    <button onClick={setEditedRows} name="done">
                        ✔
                    </button>
                </div>
            ) : (
                <button onClick={setEditedRows} name="edit">
                    ✐
                </button>
            )}
        </div>
    );
};

export const TableCell = (props: any) => {
    const { row, column, table, getValue } = props;
    const initialValue = getValue();
    const [value, setValue] = useState(typeof initialValue === "boolean" ? initialValue.toString() : initialValue);
    const columnMeta = column.columnDef.meta;
    const tableMeta = table.options.meta;

    const onBlur = () => {
        tableMeta?.updateData(row.index, column.id, value);
    };
    const onSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setValue(e.target.value);
        tableMeta?.updateData(row.index, column.id, e.target.value);
    };

    return columnMeta?.type === "select" ? (
        <select onChange={onSelectChange} value={initialValue}>
            {columnMeta?.options?.map((option: optionProps) => (
                <option key={option.value} value={option.value}>
                    {option.label}
                </option>
            ))}
        </select>
    ) : (
        <input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onBlur={onBlur}
            type={columnMeta?.type || "text"}
            className="bg-transparent w-full border-transparent border-b-sub-black focus:outline-none rounded-none text-center"
        />
    );
};

export const updateToDB = (props: any) => {
    const { shopProductCardId, coupon, productId } = props.row.original;
    const value = {
        coupon: coupon,
        product_id: productId,
    };
    const handler = async () => {
        await updateChangesToDB(shopProductCardId, value).then((res) => {
            res.status === 200 ? toast.success("업데이트 성공") : toast.error("업데이트 실패");
        });
    };
    return (
        <button onClick={handler} className="bg-main-black text-white p-2 active:bg-blue-black">
            DB 저장
        </button>
    );
};

export const sendDraft = (props: any) => {
    const sku = props.row.original.productInfo?.sku;
    // const handler = async () => {
    //     await updateChangesToDB(shopProductCardId, value).then((res) => {
    //         res.status === 200 ? toast.update("초안 보내기 성공") : toast.error("업데이트 실패");
    //     });
    // };
    return sku === undefined ? (
        <button className="bg-blue-600 text-white p-2">초안 작성</button>
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

// Assuming props.row.original is stable or doesn't change often
export function GetPrices(props: any): Prices {
    const calculatePrices = useCallback(() => {
        const { originalPrice, intlShipPrice, buyingCurrency, usCurrency, taxReductionRate, errorRate, coupon } =
            props.row.original;

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
            props.row.original.isDdp,
            props.row.original.fromUsShipping
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
