import ScrapResult from "./main";
import { getScraptResult } from "../../fetch";

export default async function Main({ params }: { params: { slug: string } }) {
    const { status, data: fetchData } = await getScraptResult(params.slug);

    return <ScrapResult fetchData={fetchData} />;
}
