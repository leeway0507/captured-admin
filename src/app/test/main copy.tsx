"use client";

import { useEffect } from "react";
import { data } from "./mockdata";
import { useRouter } from "next/navigation";

const Main = ({ data }: { data: any }) => {
    const router = useRouter();
    useEffect(() => {
        const firstContainer = document.querySelectorAll(".child-container:nth-child(11) ");
        const firstObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                entry.isIntersecting &&
                    (console.log("first-obsover", entry.target.getAttribute("aria-details")),
                    router.push(`/test/?${entry.target.getAttribute("aria-details")}`, { scroll: false }),
                    entry.target.classList.toggle("bg-red-900", entry.isIntersecting)),
                    entry;
            });
        }, {});

        firstContainer.forEach((item) => {
            firstObserver.observe(item);
        });
    }, []);

    return data.map((item, idx) => {
        return (
            <div key={idx} className="border-2">
                <div className="py-16 text-3xl text-center first-container " id={"page=" + (idx + 1)}>
                    Page : {idx + 1}
                </div>
                {item.map((item) => {
                    return (
                        <div
                            key={item.id}
                            className={`h-[100px] w-[250px] border flex-center my-8 child-container `}
                            aria-details={`${"page=" + (idx + 2)}`}>
                            <h1>{item.name}</h1>
                        </div>
                    );
                })}
            </div>
        );
    });
};

export default Main;
