import Link from "next/link";
export default function SideNav() {
    return (
        <div className="w-full text-white flex-center text-xl">
            <Link href="/production" className="w-full link-animation hover:bg-deep-gray flex-center py-4">
                <div className="">Home</div>
            </Link>
            <Link href="/production/product" className="w-full link-animation hover:bg-deep-gray flex-center py-4">
                <div className="">Product</div>
            </Link>
            <Link href="/production/order" className="w-full link-animation hover:bg-deep-gray flex-center py-4">
                <div className="">Order</div>
            </Link>
            <Link href="/dev/kream" className="w-full link-animation hover:bg-deep-gray flex-center py-4">
                <div className="">Dev</div>
            </Link>
        </div>
    );
}
