import { Table } from "@/app/order/component/table/table";
import * as api from "./component/fetch";

export default async function Main() {
    const data = await api.getOrderHistory();
    console.log(data);

    return (
        <div className="py-12">
            <Table defaultData={data} />
        </div>
    );
}
