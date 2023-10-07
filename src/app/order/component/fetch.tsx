import { CreateproductCardProps } from "@/app/types/type";

// export const getOrderHistory = async (data: CreateproductCardProps) => {
//     const req = await fetch("http://127.0.0.1:8000/api/order/get-order-history", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//         },
//         body: JSON.stringify(data),
//     });
//     return await req.json();
// };

export const getOrderRow = async () => {
    const req = await fetch("http://127.0.0.1:8000/api/admin/get-order-row");
    return await req.json();
};

export const getOrderHistory = async () => {
    const req = await fetch("http://127.0.0.1:8000/api/admin/get-order-history");
    return await req.json();
};
