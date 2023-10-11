"use server";

import { getProductByCursor } from "./fetch";

const fetccNewData = async (sku: number, page: number) => {
    const data = await getProductByCursor(sku, page);
    return data;
};

export default fetccNewData;
