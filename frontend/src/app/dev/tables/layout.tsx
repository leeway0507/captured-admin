"use client";
import { useRouter } from "next/navigation";
import { ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Link from "next/link";

function SideNav() {
    return (
        <div className="w-full text-white flex-center text-xl">
            <Link href="/dev/kream" className="w-full link-animation flex-center py-4">
                <div className="">Kream</div>
            </Link>
            <Link
                href="/dev/kream/scrap-result/result-list"
                className="w-full link-animation hover:bg-purple-500 flex-center py-4">
                <div className="">Scrap Result</div>
            </Link>
            <Link href="/dev/shop" className="w-full link-animation hover:bg-purple-500 flex-center py-4">
                <div className="">Shop</div>
            </Link>
            <Link href="/dev/shop/shop-info" className="w-full link-animation hover:bg-purple-500 flex-center py-4">
                <div className="">Shop Info</div>
            </Link>
            <Link
                href="/dev/shop/scrap-result/result-list"
                className="w-full link-animation hover:bg-purple-500 flex-center py-4">
                <div className="">Scrap Result</div>
            </Link>
            <Link href="/dev/tables" className="w-full link-animation hover:bg-purple-500 flex-center py-4">
                <div className="">Table List</div>
            </Link>
        </div>
    );
}

export default function DevLayout({ children }: { children: React.ReactNode }) {
    const router = useRouter();
    return (
        <div className="w-full h-full min-h-screen bg-purple-500 pb-6 flex flex-col relative">
            <SideNav />
            <div onClick={() => router.back()} className="absolute text-xl link-animation pt-16 z-10 left-8">
                ← 돌아가기
            </div>
            <div className="bg-white p-4 grow relative flex-center">
                <div className="h-full pt-6">{children}</div>
            </div>
            <ToastContainer position="top-right" autoClose={5000} transition={Flip} pauseOnFocusLoss={false} />
        </div>
    );
}
