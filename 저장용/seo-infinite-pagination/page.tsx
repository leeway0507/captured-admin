import NavFooter from "@/app/components/nav-footer/nav-footer";
import Main from "./main";
import * as api from "./fetch";
export default async function Page({
    params,
    searchParams,
}: {
    params: { slug: string };
    searchParams: { [key: string]: string | undefined };
}) {
    console.log("search", searchParams);
    const { data, currentPage, lastPage } = await api.getCursor(searchParams.page || 1);
    console.log("currentPage", currentPage);
    console.log("lastPage", lastPage);

    return (
        <NavFooter>
            <Main data={data} currentPage={currentPage} lastPage={lastPage} />
        </NavFooter>
    );
}
