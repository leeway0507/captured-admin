import SideNav from "./side-nav";
export default function NavFooter({ children }: { children: JSX.Element }) {
    return (
        <main className="flex min-h-screen h-full min-max-w-5xl max-w-screen">
            <div className="w-[250px] bg-main-black ">
                <SideNav />
            </div>
            <div className="grow px-8 bg-slate-50">{children}</div>
        </main>
    );
}
