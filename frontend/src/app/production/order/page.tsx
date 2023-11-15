import { Table } from "@/app/production/order/component/table/table";
import * as api from "./component/fetch";

export default async function Main() {
    const data = await api.getOrderHistory();

    return (
        <div className="py-12">
            <Table defaultData={data} />
        </div>
    );
}
