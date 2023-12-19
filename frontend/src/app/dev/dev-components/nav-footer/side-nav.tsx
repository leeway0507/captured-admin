import Link from "next/link";
export default function SideNav() {
    return (
        <div className="w-full text-white flex-center text-xl">
            <Link href="/dev/kream" className="w-full link-animation flex-center py-4">
                <div className="">Kream</div>
            </Link>

            <Link href="/dev/shop" className="w-full link-animation flex-center py-4">
                <div className="">Shop</div>
            </Link>
            <Link href="/dev/tables" className="w-full link-animation flex-center py-4">
                <div className="">Table List</div>
            </Link>
            <Link href="/dev/shop/shop-info" className="w-full link-animation flex-center py-4">
                <div className="">Shop Info</div>
            </Link>
            <Link href="/production/product" className="w-full link-animation flex-center py-4">
                <div className="">Prod</div>
            </Link>
        </div>
    );
}
