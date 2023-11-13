"use client";
import { useRouter } from "next/navigation";
import { ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function DevLayout({ children }: { children: React.ReactNode }) {
    const router = useRouter();
    return (
        <div className="w-full h-full min-h-screen bg-purple-500 py-6 flex">
            <div className="bg-white p-4 grow relative">
                <div onClick={() => router.back()} className="absolute text-xl link-animation">
                    ← 돌아가기
                </div>
                <div className="h-full pt-6">{children}</div>
            </div>
            <ToastContainer position="top-right" autoClose={5000} transition={Flip} pauseOnFocusLoss={false} />
        </div>
    );
}
