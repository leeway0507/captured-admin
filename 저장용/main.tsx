"use client";

import { data } from "./mockdata";

const Main = () => {
    return data.map((item, idx) => {
        return (
            <div key={idx} className="">
                <div className="text-3xl text-center">Page : {idx + 1}</div>
                {item.map((item) => {
                    return (
                        <div key={item.id} className="h-[100px] w-[250px] border flex-center my-8 ">
                            <h1>{item.name}</h1>
                        </div>
                    );
                })}
            </div>
        );
    });
};

export default Main;
