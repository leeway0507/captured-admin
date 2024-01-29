import ProductionTable from "./page-client";

import { Metadata } from "next";
export const metadata: Metadata = {
    title: "실제품 테이블",
    description: "...",
};

export default function Page() {
    return <ProductionTable />;
}
