"use client";
import BrandList from "./brandList";
import ShopList from "./shopList";

import { Tab } from "@headlessui/react";

function classNames(...classes: string[]) {
    return classes.filter(Boolean).join(" ");
}

const tablClass = ({ selected }: { selected: boolean }) =>
    classNames(
        "w-full rounded-lg py-2.5 font-medium leading-5 text-main-black",
        "ring-white/60 ring-offset-2 ring-offset-sub-black focus:outline-none focus:ring-2",
        selected ? "bg-white shadow" : "text-light-gray hover:bg-white/[0.12] hover:text-white"
    );

function MyTabs() {
    return (
        <Tab.Group>
            <Tab.List className="absolute top-0 flex space-x-1 rounded-xl bg-main-black p-1 min-w-[800px] max-w-[1080px]">
                <Tab className={tablClass}>브랜드</Tab>
                <Tab className={tablClass}>사이트</Tab>
            </Tab.List>
            <Tab.Panels className="pt-16">
                <Tab.Panel>
                    <BrandList />
                </Tab.Panel>
                <Tab.Panel className="h-full w-full m-auto">
                    <ShopList />
                </Tab.Panel>
            </Tab.Panels>
        </Tab.Group>
    );
}

const Page = () => {
    return (
        <div className="relative h-full w-full">
            <MyTabs />;
        </div>
    );
};

export default Page;
