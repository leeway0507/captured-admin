import SideNav from "./side-nav";
import { ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function NavFooter({ children }: { children: JSX.Element }) {
    return (
        <main className="flex min-h-screen h-full min-max-w-5xl max-w-screen">
            <div className="w-[250px] bg-purple-900	shrink-0">
                <SideNav />
            </div>
            <div className="grow px-8 bg-slate-50">
                <div className="flex flex-col h-full gap-8 w-full max-w-5xl p-8">{children}</div>
            </div>
            <ToastContainer position="top-center" autoClose={2000} transition={Flip} pauseOnFocusLoss={false} />
        </main>
    );
}
