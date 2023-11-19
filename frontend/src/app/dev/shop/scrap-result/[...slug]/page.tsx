import ProductListResult from "./product-list-result";
import ProductPageResult from "./product-page-result";
import { getProductListResult, getProductPageResult } from "../../fetch";

export default async function Main({ params }: { params: { slug: string[] } }) {
    const [type, fileName] = params.slug;

    if (type == "list") {
        const { data: ProductListData } = await getProductListResult(fileName);
        return <ProductListResult fetchData={ProductListData} />;
    }
    if (type == "page") {
        const { data: ProductPageData } = await getProductPageResult(fileName);
        return <ProductPageResult fetchData={ProductPageData} />;
    }
    return <div>로딩중</div>;
}
