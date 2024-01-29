import ListReport from "./list-report";
import PageReport from "./page-report";
import { getPlatformListReportItem, getPlatformPageReportItem } from "../../fetch-report";

export default async function Main({ params }: { params: { slug: string[] } }) {
    const [type, fileName] = params.slug;

    if (type == "list") {
        const { data: ListData } = await getPlatformListReportItem(fileName);
        return <ListReport fetchData={ListData} />;
    }
    if (type == "page") {
        const { data: PageData } = await getPlatformPageReportItem(fileName);
        return <PageReport fetchData={PageData} />;
    }
    return <div>로딩중</div>;
}
