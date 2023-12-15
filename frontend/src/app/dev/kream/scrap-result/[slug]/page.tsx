import ScrapResult from "./main";
import { getScraptResult } from "../../fetch";

export default async function Main({ params }: { params: { slug: string } }) {
    const { status, data: fetchData } = await getScraptResult(params.slug);

    console.log("fetchData");
    console.log("fetchData");
    console.log(fetchData);

    return (
        <div className="flex flex-col w-full">
            <ScrapResult fetchData={fetchData} />
        </div>
    );
}
