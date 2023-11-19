"use client";
import ShopProductList from "./shop-product-list";
import ShopProductPage from "./shop-product-page";

import { Tab } from "@headlessui/react";

function classNames(...classes: string[]) {
    return classes.filter(Boolean).join(" ");
}

const tablClass = ({ selected }: { selected: boolean }) =>
    classNames(
        "w-full rounded-lg py-2.5 font-medium leading-5 text-main-black",
        "ring-white/60 ring-offset-2 ring-offset-purple-400 focus:outline-none focus:ring-2",
        selected ? "bg-white text-purple-700 shadow" : "text-white hover:bg-white/[0.12]"
    );

function MyTabs() {
    return (
        <Tab.Group>
            <Tab.List className="absolute top-4 flex space-x-1 rounded-xl bg-purple-500 p-1 min-w-[800px] max-w-[1080px]">
                <Tab className={tablClass}>리스트 수집</Tab>
                <Tab className={tablClass}>페이지 수집</Tab>
            </Tab.List>
            <Tab.Panels className="pt-16 w-full">
                <Tab.Panel>
                    <ShopProductList />
                </Tab.Panel>
                <Tab.Panel>
                    <ShopProductPage />
                </Tab.Panel>
            </Tab.Panels>
        </Tab.Group>
    );
}

const Page = () => {
    return (
        <div className="relative flex align-center justify-center w-full">
            <MyTabs />
        </div>
    );
};

export default Page;
