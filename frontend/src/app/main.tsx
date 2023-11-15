import Link from "next/link";
export default function Main() {
    return (
        <div className="w-full h-full bg-light-gray flex-center">
            <div className="flex-center gap-16 w-[650px] h-full">
                <Link
                    href="/dev/kream"
                    className="basis-1/2 text-4xl border border-main-black rounded-lg h-[300px] flex-center hover:bg-purple-900 transition duration-500 hover:text-white">
                    Dev
                </Link>
                <Link
                    href="/production"
                    className="basis-1/2 text-4xl border border-main-black rounded-lg h-[300px] flex-center hover:bg-main-black transition duration-500  hover:text-white">
                    {" "}
                    Production
                </Link>
            </div>
        </div>
    );
}
