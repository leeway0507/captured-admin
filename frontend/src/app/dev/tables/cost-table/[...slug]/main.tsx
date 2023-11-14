"use client";
import { CostTable, productCardProps } from "./table/table";

const Main = ({ productCardList }: { productCardList: productCardProps[] }) => {
    return CostTable({ defaultData: productCardList });
};

export default Main;
