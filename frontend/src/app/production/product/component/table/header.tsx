"use client";

import Image from "next/image";

import { CreateproductCardProps } from "@/app/types/type";
import { createColumnHelper } from "@tanstack/react-table";
import { TableCell } from "@/app/components/default-table/default-header-function";
import Select from "react-select";
import envJson from "@/app/env.json";
import { toast } from "react-toastify";
import { updateProductDeploy, updateProduct, deleteProduct, uploadImageToS3 } from "../fetch";

type CategorySpec = {
    의류: string[];
    신발: string[];
    기타: string[];
    [key: string]: string[]; // Index signature
};

const columnHelper = createColumnHelper<CreateproductCardProps>();

const imgArray = () => {
    const imgArray = envJson.NEXT_PUBLIC_IMAGE_TYPE;
    return imgArray.map((v: string) => ({ value: v, label: v }));
};
const brandNameCell = (props: any) => {
    const { brand } = props.row.original;
    const options = envJson.NEXT_PUBLIC_BRAND_ARRAY;
    const defaultValue = options.find((v: { value: string; label: string }) => v.label === brand);
    return <Select defaultValue={defaultValue} options={options} className="min-w-[150px] max-w-full" />;
};

const categoryArray = () => {
    const categoryArray = envJson.NEXT_PUBLIC_CATEGORY;
    return categoryArray.map((v: string) => ({ value: v, label: v }));
};

const categorySpecCell = (props: any) => {
    const { categorySpec, category } = props.row.original;
    const categorySpecObject: CategorySpec = envJson.NEXT_PUBLIC_CATEGORY_SPEC;
    const categorySpecData = categorySpecObject[category];
    const options = categorySpecData.map((v: string) => ({ value: v, label: v }));

    const defaultValue = options.find((v: { value: string; label: string }) => v.value === categorySpec);

    return <Select defaultValue={defaultValue} options={options} className="min-w-[100px] max-w-full" />;
};

const handleCandidate = (event: any, sku: number, deploy: number) => {
    // const { sku, deploy } = event.target.dataset;
    const reverseStatus = deploy === 1 ? 0 : 1;

    event.target.dataset.deploy = reverseStatus;

    updateProductDeploy(sku, reverseStatus).then((res) => {
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

const handleUpdateProduct = (props: any) => {
    const rowData = props.row.original;

    const handler = async () => {
        await updateProduct(rowData).then((res) => {
            res.status === 200 ? toast.success("업데이트 성공") : toast.error("업데이트 실패");
        });
    };
    return (
        <button onClick={handler} className="bg-main-black text-white p-2 active:bg-blue-black whitespace-nowrap">
            변경 저장
        </button>
    );
};

const handleDeleteProduct = (props: any) => {
    const { sku } = props.row.original;
    const handler = async () => {
        confirm(`sku : ${sku} 제품을 삭제합니다.`) &&
            (await deleteProduct(sku).then((res) => {
                res.status === 200 ? toast.success("업데이트 성공") : toast.error("업데이트 실패");
            }));
    };
    return (
        <button onClick={handler} className="bg-rose-600 text-white p-2 active:bg-blue-black whitespace-nowrap">
            DB 제거
        </button>
    );
};

const reloadImage = (sku: number) => {
    const img = document.getElementById(sku.toString()) as HTMLImageElement;
    img.src = `${process.env.NEXT_PUBLIC_MOBILE_IMAGE_URL}/product/${sku}/thumbnail.png`;
};

const UploadImage = (props: any) => {
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

const features = (props: any) => {
    return (
        <div className="flex flex-col h-[200px] justify-evenly">
            {handleUpdateProduct(props)}
            {UploadImage(props)}
            {handleDeleteProduct(props)}
        </div>
    );
};

export const productCardColumns = [
    columnHelper.accessor("sku", {
        header: "Sku",
        cell: (props) => {
            const { sku, deploy } = props.row.original;
            if (sku === undefined) {
                return toast.error("sku가 없습니다.");
            }
            return (
                <button
                    onClick={(e) => handleCandidate(e, sku, deploy!)}
                    className={`${
                        deploy === 0 ? "bg-rose-300" : "bg-green-300"
                    } h-[180px] w-[80px] text-sm flex-center flex-col`}
                    data-sku={sku}
                    data-deploy={deploy}>
                    <div>{deploy === 0 ? "미전시" : "전시중"}</div>
                    <div>sku : {props.getValue()}</div>
                </button>
            );
        },
        filterFn: (row, columnId, value, addMeta) => {
            return row.original.sku === Number(value);
        },
    }),
    columnHelper.display({
        header: "Img",
        cell: (props) => {
            const { sku } = props.row.original;
            const productImgUrl = `${process.env.NEXT_PUBLIC_MOBILE_IMAGE_URL}/product/${sku}/thumbnail.png`;
            return (
                <div className="relative h-[180px] w-[180px] ">
                    <Image
                        id={sku!.toString()}
                        src={productImgUrl}
                        alt={props.row.original.productName}
                        fill
                        sizes="150px"
                        style={{ objectFit: "contain" }}
                    />
                </div>
            );
        },
    }),
    columnHelper.display({
        header: "기능",
        cell: features,
    }),
    columnHelper.accessor("brand", {
        header: "브랜드",
        cell: brandNameCell,
    }),
    columnHelper.accessor("productName", {
        header: "제품명",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("productId", {
        header: "제품 아이디",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("price", {
        header: "판매가",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("shippingFee", {
        header: "배송비",
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor("intl", {
        header: "배송",
        cell: TableCell,
        meta: {
            type: "select",
            options: [
                { value: true, label: "해외" },
                { value: false, label: "국내" },
            ],
        },
    }),
    columnHelper.accessor("imgType", {
        header: "이미지 타입",
        cell: TableCell,
        meta: {
            type: "select",
            options: imgArray(),
        },
    }),
    columnHelper.accessor("color", {
        header: "색상",
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor("category", {
        header: "카테고리",
        cell: TableCell,
        meta: {
            type: "select",
            options: categoryArray(),
        },
    }),
    columnHelper.accessor("categorySpec", {
        header: "Category",
        cell: categorySpecCell,
    }),
];
