"use client";
import envJson from "@/app/env.json";
import Select from "react-select";
import { useState } from "react";
import { updateProductData, patchProductData, deleteProductData, uploadImageToS3 } from "../fetch";
import { toast } from "react-toastify";
import { CreateproductCardProps } from "@/app/types/type";

type CategorySpec = {
    의류: string[];
    신발: string[];
    기타: string[];
    [key: string]: string[]; // Index signature
};

export const imgArray = () => {
    const imgArray = envJson.NEXT_PUBLIC_IMAGE_TYPE;
    return imgArray.map((v: string) => ({ value: v, label: v }));
};

export const BrandNameCell = (props: any) => {
    const { row, table } = props;
    const { brand, korBrand } = props.row.original;
    const options = envJson.NEXT_PUBLIC_BRAND_ARRAY;
    const korBrandArr = envJson.NEXT_PUBLIC_KOR_BRAND_OBJECT;
    const tableMeta = table.options.meta;

    const onSelectChange = (e: any) => {
        tableMeta?.updateData(row.index, "brand", e.label);
        tableMeta?.updateData(row.index, "korBrand", korBrandArr[e.value as keyof typeof korBrandArr]);
    };
    const defaultValue = options.find((v: { value: string; label: string }) => v.label === brand);
    return (
        <>
            <Select
                defaultValue={defaultValue}
                onChange={onSelectChange}
                options={options}
                className="min-w-[150px] max-w-full"
            />
            <div className="pt-4 text-sm">{korBrand}</div>
        </>
    );
};

export const categoryArray = () => {
    const categoryArray = envJson.NEXT_PUBLIC_CATEGORY;
    return categoryArray.map((v: string) => ({ value: v, label: v }));
};

export const CategorySpecCell = (props: any) => {
    const { row, column, table, getValue } = props;
    const { categorySpec, category } = row.original;
    const categorySpecObject: CategorySpec = envJson.NEXT_PUBLIC_CATEGORY_SPEC;
    const categorySpecData = categorySpecObject[category];
    const options = categorySpecData.map((v: string) => ({ value: v, label: v }));
    const tableMeta = table.options.meta;
    const initialValue = getValue();

    const [value, setValue] = useState(initialValue);
    const onSelectChange = (e: any) => {
        setValue(e.value);
        tableMeta?.updateData(row.index, column.id, e.value);
    };

    const defaultValue = options.find((v: { value: string; label: string }) => v.value === categorySpec);

    return (
        <Select
            defaultValue={defaultValue}
            onChange={onSelectChange}
            options={options}
            className="min-w-[100px] max-w-full"
        />
    );
};

export const handleCandidate = (event: any, sku: number, deploy: number) => {
    // const { sku, deploy } = event.target.dataset;
    const reverseStatus = deploy === 1 ? 0 : 1;

    event.target.dataset.deploy = reverseStatus;

    patchProductData(sku, "deploy", reverseStatus).then((res) => {
        const candidateClass = "h-[180px] w-[80px] text-sm flex-center flex-col";

        if (res.status === 200) {
            event.target.className =
                reverseStatus === 0 ? `bg-rose-300 ${candidateClass}` : `bg-green-300 ${candidateClass}`;
            event.target.dataset.deploy = reverseStatus;
            toast.success("업데이트 성공");
        } else {
            toast.error("업데이트 실패");
        }
    });
};

export const handleUpdateProduct = (props: any) => {
    const rowData: CreateproductCardProps = props.row.original;
    const brand = rowData.brand;
    const korBrand = rowData.korBrand;
    const productName = rowData.productName;
    const korProductName = rowData.korProductName;
    const productId = rowData.productId;

    const rowDataCopied = JSON.parse(JSON.stringify(rowData));
    rowDataCopied.searchInfo = `${brand} ${korBrand} ${productName} ${korProductName} ${productId}`;

    const handler = async () => {
        await updateProductData(rowDataCopied).then((res) => {
            res.status === 200 ? toast.success("업데이트 성공") : toast.error("업데이트 실패");
        });
    };
    return (
        <button onClick={handler} className="bg-main-black text-white p-2 active:bg-blue-black whitespace-nowrap">
            변경 저장
        </button>
    );
};

export const handleDeleteProduct = (props: any) => {
    const { sku } = props.row.original;
    const handler = async () => {
        confirm(`sku : ${sku} 제품을 삭제합니다.`) &&
            (await deleteProductData(sku).then((res) => {
                if (res.status === 200) return toast.success("업데이트 성공");
                res.status === 409
                    ? toast.warning("Intergrity Error: \n 다른 테이블에 연결된 데이터가 있습니다.")
                    : toast.error("업데이트 실패");
            }));
    };
    return (
        <button onClick={handler} className="bg-rose-600 text-white p-2 active:bg-blue-black whitespace-nowrap">
            DB 제거
        </button>
    );
};

export const reloadImage = (sku: number) => {
    const img = document.getElementById(sku.toString()) as HTMLImageElement;
    img.src = `${process.env.NEXT_PUBLIC_MOBILE_IMAGE_URL}/product/${sku}/thumbnail.webp`;
};

export const UploadImage = (props: any) => {
    const { sku } = props.row.original;
    const handler = async () => {
        await uploadImageToS3(sku).then((res) => {
            switch (res.status) {
                case 200:
                    reloadImage(sku);
                    return toast.success("이미지 업로드 성공");

                case 404:
                    return toast.warn("파일이 존재하지 않습니다.");

                default:
                    return toast.error("이미지 업로드 실패");
            }
        });
    };
    return (
        <button onClick={handler} className="bg-amber-600 text-white p-2 active:bg-blue-black">
            사진 저장
        </button>
    );
};
