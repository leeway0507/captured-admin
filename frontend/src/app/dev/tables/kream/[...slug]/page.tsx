import Main from "./main";
import { getKreamProdCardByBrandName } from "./fetch";

export default async function Page({
    params,
    searchParams,
}: {
    params: { slug: string[] };
    searchParams: { [key: string]: string | undefined };
}) {
    const [searchType, content] = params.slug;

    const contentDecoded = decodeURIComponent(content);
    const kreamProductCardList = await getKreamProdCardByBrandName(contentDecoded);
    return (
        <>
            <Main kreamProductCardList={kreamProductCardList.data} />
        </>
    );
}
