"use client";
import { useSearchParams } from "next/navigation";
import { getProduct } from "@/app/production/product/component/fetch";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Select from "react-select";

const ProductInfoPagination = ({
    currentPage,
    lastPage,
    setPageData,
}: {
    currentPage: number;
    lastPage: number;
    setPageData: (v: any) => void;
}) => {
    const router = useRouter();
    const [pageSize, setPageSize] = useState<number>(50);

    const pageHandler = (page: number) => {
        return router.push(`/production/product?page=${page}&limit=${pageSize}`);
    };
    const searchParams = useSearchParams();

    useEffect(() => {
        const page = searchParams.get("page");
        const limit = searchParams.get("limit");

        if (page && limit) {
            getProduct(Number(page), Number(limit)).then((res) => {
                setPageData(res.data);
            });
        }
    }, [searchParams, setPageData]);

    return (
        <div className="flex items-center gap-2 ">
            <button
                className="border rounded p-1 disabled:opacity-50"
                onClick={() => pageHandler(0)}
                disabled={currentPage === 1}>
                {"<<"}
            </button>
            <button
                className="border rounded p-1 disabled:opacity-50"
                onClick={() => (pageHandler(currentPage - 1), window.scrollTo(0, 0))}
                disabled={currentPage === 1}>
                {"<"}
            </button>
            <button
                className="border rounded p-1 disabled:opacity-50"
                onClick={() => (pageHandler(currentPage + 1), window.scrollTo(0, 0))}
                disabled={currentPage === lastPage}>
                {">"}
            </button>
            <button
                className="border rounded p-1 disabled:opacity-50"
                onClick={() => (pageHandler(lastPage), window.scrollTo(0, 0))}
                disabled={currentPage === lastPage}>
                {">>"}
            </button>
            <span className="flex items-center gap-1 disabled:opacity-50">
                <div>Page</div>
                <strong>
                    {currentPage} of {lastPage}
                </strong>
            </span>
            <span className="flex items-center gap-1 disabled:opacity-50">
                | Go to page:
                <input
                    type="number"
                    defaultValue={currentPage}
                    onChange={(e) => {
                        const page = e.target.value ? Number(e.target.value) : 0;
                        router.push(`/production/product?page=${page}&limit=${pageSize}`);
                    }}
                    className="border p-1 rounded w-16"
                />
            </span>
            <Select
                instanceId={"select"}
                className="z-50"
                defaultValue={{ value: "50", label: "Show 50" }}
                options={[
                    { value: "50", label: "Show 50" },
                    { value: 100, label: "Show 100" },
                    { value: 200, label: "Show 200" },
                ]}
                onChange={(e: any) => {
                    setPageSize(Number(e.value));
                }}
            />
        </div>
    );
};

export default ProductInfoPagination;
