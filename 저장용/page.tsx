import NavFooter from "@/app/components/nav-footer/nav-footer";
import Main from "./main";
export default function Page({
    params,
    searchParams,
}: {
    params: { slug: string };
    searchParams: { [key: string]: string | undefined };
}) {
    return (
        <NavFooter>
            <Main />
        </NavFooter>
    );
}
