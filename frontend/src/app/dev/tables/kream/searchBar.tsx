"use client";
import { toast } from "react-toastify";
import Select from "react-select";
import { useState } from "react";
import { useRouter } from "next/navigation";

const SearchBar = () => {
    const router = useRouter();
    const [search, setSearch] = useState<{ searchType: string; content: string }>({
        searchType: "productId",
        content: "",
    });

    const handleSubmit = (search: { searchType: string; content: string }) => {
        if (search.content === "") {
            return toast.error("값을 입력해주세요.");
        }
        router.push(`/dev/tables/kream/${search.searchType}/${search.content}`);
    };

    const selectCat = [
        { value: "productId", label: "제품 아이디" },
        { value: "kreamId", label: "크림아이디" },
        { value: "brandName", label: "브랜드명" },
    ];

    return (
        <div className="flex gap-8 justify-space">
            <div className="min-w-[300px] flex flex-col">
                <div className="text-xl">검색 타입 선정</div>
                <Select
                    className="z-50"
                    defaultValue={selectCat[0]}
                    instanceId="shopName"
                    options={selectCat}
                    onChange={(e: any) => {
                        setSearch({ ...search, searchType: e.value });
                    }}
                />
            </div>
            <div className="min-w-[150px] flex flex-col">
                <label htmlFor="brandName">입력해주세요.</label>
                <input
                    type="text"
                    name="brandName"
                    id="brandName"
                    onChange={(e) => {
                        setSearch({ ...search, content: e.target.value });
                    }}
                    className="border border-main-black h-[50px] rounded-md px-4"
                />
            </div>

            <button className="black-bar-with-disabled min-w-[150px] text-xl " onClick={() => handleSubmit(search)}>
                요청하기
            </button>
        </div>
    );
};

export default SearchBar;
