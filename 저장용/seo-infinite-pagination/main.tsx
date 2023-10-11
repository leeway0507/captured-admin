"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

// 실행원리
// server component 최초 페이지 생성 => client component로 페이지 변동 감지 => 특정 엘리먼트 intersection 시 page params 변동
// => server component에서 page params에 따른 데이터를 불러옴 => client component로 데이터 전달 => 반복

const Main = ({ data, currentPage, lastPage }: { data: any; currentPage: any; lastPage: any }) => {
    // data = 페이지 대응하는 데이터
    // currentPage = 현재 페이지
    // lastPage = 마지막 페이지

    // page param 지정을 위한 router
    const router = useRouter();

    // 더보기 자동 실행용도로 사용
    const ref = useRef(null);

    // 페이지 저장 (페이지 번호 : 데이터)
    const [localData, setLocalData] = useState({ [currentPage]: data });

    // intersection observer 사용
    useEffect(() => {
        // 페이지 번호가 localData에 없으면 localData에 저장
        setLocalData((localData) => ({ ...localData, [currentPage]: data }));

        // intersection observer 사용하기

        // page-container의 마지막 div를 트거로 지정
        const firstContainer = document.querySelectorAll(".page-container>div:last-child");

        // Obersever 생성 및 트리거 시 수행할 함수 작성(router.push로 page params 업데이트)
        const firstObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                entry.isIntersecting &&
                    (router.push(`/test/?${entry.target.getAttribute("data-next")}`, { scroll: false }),
                    entry.target.classList.toggle("bg-red-900", entry.isIntersecting));
            });
        }, {});

        // 트리거로 지정한 div들을 Observe 시작
        firstContainer.forEach((item) => {
            firstObserver.observe(item);
        });

        // 더보기 실행을 위한 observer 작성
        // router.refresh 됨에 따라 useEffect를 다시 작동시켜 페이지를 불러오는 방식
        const lastObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                entry.isIntersecting && router.refresh();
            });
        }, {});

        // 마지막 페이지 도달 시 더보기 실행 방지
        currentPage < lastPage ? lastObserver.observe(ref.current!) : lastObserver.unobserve(ref.current!);
    }, [data, currentPage, lastPage, router]);

    console.log("localData:로컬데이터", localData);
    console.log("localData:로컬데이터", Object.keys(localData).includes("1"));

    return (
        <>
            <Link
                href={`/test/?page=${currentPage - 1}`}
                className={`${
                    Object.keys(localData).includes("1") ? "hidden" : "block"
                } h-[100px] w-full bg-deep-gray`}>
                Top:{Object.keys(localData).includes("1")}
            </Link>
            <div className="flex flex-col items-center">
                {Object.entries(localData).map((item, idx) => {
                    return (
                        <div className="page-container" key={item[0] + "k" + idx}>
                            {item[1].map((data: any) => {
                                return (
                                    <div
                                        key={data.sku}
                                        className="h-[300px] w-[700px] border bg-deep-gray flex-center my-32 "
                                        data-prev={`page=${parseInt(item[0]) - 1}`}
                                        data-next={`page=${
                                            parseInt(item[0]) + 1 <= lastPage ? parseInt(item[0]) + 1 : lastPage
                                        } `}>
                                        <div className="text-3xl flex-center">{data.sku}</div>
                                        <div className="text-3xl flex-center">page={parseInt(item[0])}</div>
                                    </div>
                                );
                            })}
                        </div>
                    );
                })}
                <div ref={ref} className="h-[200px] w-[1000px] bg-red">
                    LastPage
                </div>
            </div>
        </>
    );
};

export default Main;
