"use client";
import { useEffect, useRef, useState } from "react";
import { RestartSavingCreatelog, RestartSavingLastScrapedFiles } from "./fetch";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";

export const handleSavingCreatelog = async (
    scrapName: string,
    setName: (scrapName: string) => void,
    enableButton: () => void,
    disableButton: () => void
) => {
    if (scrapName === "") {
        return toast.error("스크랩 주소를 적어주세요.");
    }

    const start = confirm(`브랜드네임 [${scrapName}]이 맞으면 시작합니다.`);

    if (!start) {
        return;
    }

    disableButton();
    await RestartSavingCreatelog(scrapName)
        .then((res) => {
            res.status === 200 ? setName(scrapName) : toast.error("에러 발생");
            enableButton();
        })
        .catch((e) => {
            toast.error("네트워크 에러 발생");
            enableButton();
        });
};

export default function ReproduceReport() {
    const router = useRouter();
    const submitRef2 = useRef<HTMLButtonElement>(null);
    const [brandName, setBrandName] = useState("");
    const [scrapName, setScrapName] = useState("");

    const [urlParam, setUrlParam] = useState("");

    const enableButton = () => {
        if (submitRef2.current) {
            submitRef2.current.disabled = false;
        }
    };

    const disableButton = () => {
        if (submitRef2.current) {
            submitRef2.current.disabled = true;
        }
    };

    useEffect(() => {
        if (urlParam === "") return;
        router.push(`/dev/kream/scrap-result/${urlParam}`);
    }, [urlParam, router]);

    const handleRestartSavingFiles = async () => {
        RestartSavingLastScrapedFiles(brandName).then((res) => {
            res.status === 200 ? (toast.success("요청 성공"), setScrapName(res.data)) : toast.error("에러 발생");
        });
    };

    return (
        <>
            <div className="flex pt-4 pb-24 gap-8 justify-between">
                <div className="min-w-[200px] flex flex-col">
                    <label htmlFor="brandName">수집자료 Parquet으로 저장</label>
                    <input
                        type="text"
                        name="brandName"
                        id="brandName"
                        placeholder="브랜드이름 ex) adidas"
                        onChange={(e) => {
                            setBrandName(e.target.value);
                        }}
                        value={brandName}
                        className="border border-main-black h-[50px] rounded-md px-4"
                    />
                </div>
                <button className="black-bar-with-disabled min-w-[150px] text-xl" onClick={handleRestartSavingFiles}>
                    요청하기
                </button>
                <div className="min-w-[200px] flex flex-col">
                    <label htmlFor="brandName">수집 보고서 생산</label>
                    <input
                        type="text"
                        name="brandName"
                        id="brandName"
                        placeholder="231010-112233-adidas"
                        onChange={(e) => {
                            setScrapName(e.target.value);
                        }}
                        value={scrapName}
                        className="border border-main-black h-[50px] rounded-md px-4"
                    />
                </div>
                <button
                    ref={submitRef2}
                    className="black-bar-with-disabled min-w-[150px] text-xl"
                    onClick={() => handleSavingCreatelog(scrapName, setUrlParam, enableButton, disableButton)}>
                    요청하기
                </button>
            </div>
        </>
    );
}
