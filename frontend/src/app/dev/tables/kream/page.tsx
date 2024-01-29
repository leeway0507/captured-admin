import SearchBar from "./searchBar";
import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "크림 테이블",
    description: "...",
};
const Page = () => {
    return (
        <div className="w-full flex-center">
            <SearchBar />
        </div>
    );
};

export default Page;
