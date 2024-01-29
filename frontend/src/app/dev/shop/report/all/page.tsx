import { MyTabs } from "./page-client";
import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "스토어 결과",
    description: "...",
};
const Page = () => {
    return <MyTabs />;
};

export default Page;
