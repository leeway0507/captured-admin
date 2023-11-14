"use client";
import { loadShopName, loadScrapedBrandName } from "../../shop/fetch";
import { toast } from "react-toastify";
import Select from "react-select";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";

const Page = () => {
    const router = useRouter();
    const [search, setSearch] = useState<{ shopName: string; brandName: string }>({ shopName: "", brandName: "" });
    const [shopList, setShopList] = useState<{ value: string; label: string }[]>([]);
    const [brandList, setBrandList] = useState<{ value: string; label: string }[]>([]);

    useEffect(() => {
        loadShopName().then((res) => {
            setShopList(res.data.map((option: string) => ({ value: option, label: option })));
        });
    }, []);

    useEffect(() => {
        if (search.shopName !== "")
            loadScrapedBrandName(search.shopName).then((res) => {
                setBrandList(res.data.map((option: string) => ({ value: option, label: option })));
            });
    }, [search.shopName]);

    const handleSubmit = (search: { shopName: string; brandName: string }) => {
        if (search.shopName === "") {
            return toast.error("스크랩할 샵을 선택하세요.");
        }
        if (search.brandName === "") {
            return toast.error("브랜드 네임을 입력해주세요.");
        }
        router.push(`/dev/tables/candidate-table/${search.shopName}/${search.brandName}`);
    };

    return (
        <div className="h-full flex-center">
            <div className="flex gap-8 justify-space">
                <div className="min-w-[300px] flex flex-col">
                    <div className="text-xl">스크랩 샵 이름</div>
                    <Select
                        instanceId="shopName"
                        options={shopList}
                        onChange={(e: any) => {
                            setSearch({ ...search, shopName: e.value });
                        }}
                    />
                </div>
                <div className="min-w-[300px] flex flex-col">
                    <div className="text-xl">브랜드 이름</div>
                    <Select
                        instanceId="brandName"
                        options={brandList}
                        isMulti
                        onChange={(e: any) => {
                            const result = e.reduce(
                                (
                                    accumulator: string,
                                    currentValue: { value: string; label: string },
                                    index: number
                                ) => {
                                    const separator = index === e.length - 1 ? "" : ",";
                                    return accumulator + currentValue.value + separator;
                                },
                                ""
                            );
                            setSearch({ ...search, brandName: result });
                        }}
                    />
                    <div>{search.brandName}</div>
                </div>
                <button className="black-bar-with-disabled min-w-[150px] text-xl " onClick={() => handleSubmit(search)}>
                    요청하기
                </button>
            </div>
        </div>
    );
};

export default Page;
