"use client";
import SideNav from "./side-nav";
import { ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
export default function NavFooter({ children }: { children: JSX.Element }) {
    return (
        <main className="w-full h-full min-h-screen bg-main-black pb-6 flex flex-col relative">
            <SideNav />
            <div className="bg-white py-4 px-4 items-stretch flex grow">{children}</div>
            <ToastContainer position="top-left" autoClose={5000} transition={Flip} pauseOnFocusLoss={false} />
        </main>
    );
}
