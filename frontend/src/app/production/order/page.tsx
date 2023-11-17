import { OrderHistoryTable } from "./table/order-history-table";
import { getOrderHistory } from "./fetch";

export default async function Main() {
    const data = await getOrderHistory();

    return (
        <div className="py-12">
            <OrderHistoryTable tableData={data.data} />
        </div>
    );
}
