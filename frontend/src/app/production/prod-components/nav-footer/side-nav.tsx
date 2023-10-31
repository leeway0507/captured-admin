import Link from "next/link";
export default function SideNav() {
    return (
        <div className="py-16 w-full text-white flex-left text-2xl flex-col sticky top-0">
            <Link href="/production" className="w-full link-animation hover:bg-deep-gray flex-center py-8">
                <div className="">Home</div>
            </Link>
            <Link href="/production/product" className="w-full link-animation hover:bg-deep-gray flex-center py-8">
                <div className="">Product</div>
            </Link>
            <Link href="/production/order" className="w-full link-animation hover:bg-deep-gray flex-center py-8">
                <div className="">Order</div>
            </Link>
            <Link href="/production/test" className="w-full link-animation hover:bg-deep-gray flex-center py-8">
                <div className="">Test</div>
            </Link>
        </div>
    );
}
