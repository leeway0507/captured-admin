import Link from "next/link";
export default function SideNav() {
    return (
        <div className="py-16 w-full h-full bg-stone-700 text-white flex-left text-2xl flex-col">
            <Link href="/" className="w-full link-animation hover:bg-stone-200 flex-center py-8">
                <div className="">Home</div>
            </Link>
            <Link href="/product" className="w-full link-animation hover:bg-stone-200 flex-center py-8">
                <div className="">Product</div>
            </Link>
        </div>
    );
}
