import ListReport from "./list-report";
import PageReport from "./page-report";
import { getScrapListReport, getScrapPageReport } from "../../fetch";

export default async function Main({ params }: { params: { slug: string[] } }) {
    const [type, fileName] = params.slug;

    if (type == "list") {
        const { data: ListData } = await getScrapListReport(fileName);
        console.log(ListData);
        return <ListReport fetchData={ListData} />;
    }
    if (type == "page") {
        const { data: PageData } = await getScrapPageReport(fileName);
        return <PageReport fetchData={PageData} />;
    }
    return <div>로딩중</div>;
}
