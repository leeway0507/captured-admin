import Link from "next/link";
export default function SideNav() {
    return (
        <div className="py-16 w-full text-white flex-left text-2xl flex-col sticky top-0">
            <Link href="/dev" className="w-full link-animation hover:bg-purple-500 flex-center py-4">
                <div className="">Home</div>
            </Link>
            <Link href="/dev/kream" className="w-full link-animation hover:bg-purple-500 flex-center py-4">
                <div className="">Kream</div>
            </Link>
            <Link
                href="/dev/kream/scrap-result/result-list"
                className="w-full link-animation hover:bg-purple-500 flex-center py-4">
                <div className="">Scrap Result</div>
            </Link>
            <Link href="/dev/order" className="w-full link-animation hover:bg-purple-500 flex-center py-4">
                <div className="">Order</div>
            </Link>
            <Link href="/dev/test" className="w-full link-animation hover:bg-purple-500 flex-center py-4">
                <div className="">Test</div>
            </Link>
        </div>
    );
}
