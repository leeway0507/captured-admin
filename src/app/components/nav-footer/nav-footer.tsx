import SideNav from "./side-nav";
export default function NavFooter({ children }: { children: JSX.Element }) {
    return (
        <main className="flex h-screen max-w-[1440px] m-auto">
            <div className="w-[250px]">
                <SideNav />
            </div>
            <div className="grow px-8">{children}</div>
        </main>
    );
}
