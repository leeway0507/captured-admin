import NavFooter from "../dev-components/nav-footer/nav-footer";
import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "스토어 수집",
    description: "...",
};
export default function DevLayout({ children }: { children: React.ReactNode }) {
    return (
        <NavFooter>
            <>{children}</>
        </NavFooter>
    );
}
