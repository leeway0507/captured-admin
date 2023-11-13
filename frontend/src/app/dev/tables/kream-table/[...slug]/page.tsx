import Main from "./main";
import { getKreamProductCardList } from "./fetch";

export default async function Page({
    params,
    searchParams,
}: {
    params: { slug: string[] };
    searchParams: { [key: string]: string | undefined };
}) {
    const [searchType, content] = params.slug;

    const searchTypeDecoded = decodeURIComponent(searchType);
    const contentDecoded = decodeURIComponent(content);
    const kreamProductCardList = await getKreamProductCardList(searchTypeDecoded, contentDecoded);

    return (
        <>
            <Main kreamProductCardList={kreamProductCardList.data} />
        </>
    );
}
