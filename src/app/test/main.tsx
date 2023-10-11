import ClientComponent from "./client";
import * as api from "./fetch";

const Main = async () => {
    const initData = await api.getProduct();

    return <ClientComponent initData={initData} />;
};

export default Main;
