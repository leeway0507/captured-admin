import Link from "next/link";
export default function SideNav() {
    return (
        <div className="w-full text-white flex-center text-xl">
            <Link href="/dev/kream" className="w-full link-animation flex-center py-4">
                <div className="">Kream</div>
            </Link>
            <Link href="/dev/kream/scrap-result/result-list" className="w-full link-animation flex-center py-4">
                <div className="">Scrap Result</div>
            </Link>
            <Link href="/dev/shop" className="w-full link-animation flex-center py-4">
                <div className="">Shop</div>
            </Link>
            <Link href="/dev/shop/shop-info" className="w-full link-animation flex-center py-4">
                <div className="">Shop Info</div>
            </Link>
            <Link href="/dev/shop/scrap-result/result-list" className="w-full link-animation flex-center py-4">
                <div className="">Scrap Result</div>
            </Link>
            <Link href="/dev/tables" className="w-full link-animation flex-center py-4">
                <div className="">Table List</div>
            </Link>
        </div>
    );
}
