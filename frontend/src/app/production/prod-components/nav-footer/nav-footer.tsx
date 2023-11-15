"use client";
import SideNav from "./side-nav";
import { ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
export default function NavFooter({ children }: { children: JSX.Element }) {
    return (
        <main className="flex min-h-screen h-full min-max-w-5xl max-w-screen">
            <div className="w-[250px] bg-main-black ">
                <SideNav />
            </div>
            <div className="grow px-8 bg-slate-50">{children}</div>
            <ToastContainer position="top-right" autoClose={5000} transition={Flip} pauseOnFocusLoss={false} />
        </main>
    );
}
