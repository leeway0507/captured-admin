import NavFooter from "./dev-components/nav-footer/nav-footer";
export default function DevLayout({ children }: { children: React.ReactNode }) {
    return (
        <NavFooter>
            <>{children}</>
        </NavFooter>
    );
}
