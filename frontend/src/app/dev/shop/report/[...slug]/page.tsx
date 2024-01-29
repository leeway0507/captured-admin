import ProductListResult from "./product-list-result";
import ProductPageResult from "./product-page-result";
import { getShopListReportItem, getShopPageReportItem } from "../../fetch-report";
import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "스토어 결과 상세",
    description: "...",
};

export default async function Main({ params }: { params: { slug: string[] } }) {
    const [type, fileName] = params.slug;

    if (type == "list") {
        const { data: ProductListData } = await getShopListReportItem(fileName);
        return <ProductListResult fetchData={ProductListData} />;
    }
    if (type == "page") {
        const { data: ProductPageData } = await getShopPageReportItem(fileName);
        return <ProductPageResult fetchData={ProductPageData} />;
    }
    return <div>로딩중</div>;
}
