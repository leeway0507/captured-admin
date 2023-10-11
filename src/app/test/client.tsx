"use client";
import { Table } from "@/app/components/table/table";
import * as api from "./fetch";
import { CreateproductCardProps } from "@/app/types/type";

import { useState, useEffect } from "react";
import { useInView } from "react-intersection-observer";
import Spinner from "./spinner";
import fetccNewData from "./action";
import { useRouter } from "next/navigation";

const ClientComponent = ({ initData }: { initData: CreateproductCardProps[] }) => {
    const router = useRouter();
    const { ref, inView, entry } = useInView({
        /* Optional options */
        threshold: 0,
    });
    const [data, setData] = useState<CreateproductCardProps[]>(() => initData);

    const [page, setPage] = useState<number>(1);
    const [prevSku, setPrevSku] = useState<number>(0);

    useEffect(() => {
        const nextPage = page + 1;
        const cursor = data.slice(-1)[0];
        setPrevSku(cursor.sku);

        if (cursor.sku !== prevSku) {
            fetccNewData(cursor.sku, nextPage).then((res) => {
                setData((data) => [...data, ...res]);
                console.log(data.length, res.length);
            });
            setPage(nextPage);
            console.log("--cursor--", cursor.sku, prevSku);
            router.push(`?sku=${cursor.sku}&page=${nextPage}`, { scroll: false });
        }
    }, [inView]);

    if (data.length == 0) return <></>;
    return (
        <>
            <div className={`flex flex-col justify-end`}>
                <div className="">
                    <div className="sticky top-[50px] z-50 bg-black text-white">{`현재 Inview : ${inView} `}</div>

                    <Table defaultData={data} />
                </div>
                <div className="flex text-blue-500 text-3xl w-full h-[100px]" ref={ref}>
                    <Spinner />
                </div>
            </div>
        </>
    );
};

export default ClientComponent;
