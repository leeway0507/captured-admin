import Link from "next/link";
export default function SideNav() {
    return (
        <div className="py-16 w-full text-white flex-left text-2xl flex-col sticky top-0">
            <Link href="/dev/kream" className="w-full link-animation hover:bg-purple-500 flex-center py-4">
                <div className="">Kream</div>
            </Link>
            <Link
                href="/dev/kream/scrap-result/result-list"
                className="w-full link-animation hover:bg-purple-500 flex-center py-4">
                <div className="">Scrap Result</div>
            </Link>
            <div className="py-8"></div>
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
        </div>
    );
}
