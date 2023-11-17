"use client";
import { productCardColumns } from "./header";
import { shopInfoProps } from "@/app/dev/shop/type";
import { productCardProps } from "../../../candidate-table/[...slug]/main";

import DefaultTable from "@/app/components/default-table/default-table";

export interface costTableDataProps extends productCardProps {
    errorRate: number;
    cardRate: number;
    VATRate: number;
    customRate: number;
    buyingCurrency: number;
    usCurrency: number;
    productInfo: productInfoProps;
    shopInfo: shopInfoProps;
}

interface costTableDataSetProps {
    shopInfos: shopInfoProps[];
    dbData: productCardProps[];
    currency: { data: { [key: string]: any }; updatedAt: Date };
}

interface productInfoProps {
    sku: number;
    productId: string;
    shippingFee: number;
    price: number;
}

const createTableData = (costTableDataSet: costTableDataSetProps, productInfo: productInfoProps[]) => {
    const { shopInfos, dbData, currency } = costTableDataSet;

    const buyingCurrency = currency.data;
    return dbData.map((row) => {
        const shopInfo = shopInfos.find((shopInfo) => shopInfo.shopName === row.shopName);
        const product = productInfo.find((productInfo) => productInfo.productId === row.productId);

        return {
            ...row,
            errorRate: 1.025,
            cardRate: 0.03,
            VATRate: 0.1,
            customRate: 0.13,
            buyingCurrency: buyingCurrency[row.originalPriceCurrency],
            usCurrency: buyingCurrency["USD"],
            productInfo: product,
            shopInfo: shopInfo,
        };
    });
};

export const CostTable = ({
    costTableDataSet,
    productInfo,
}: {
    costTableDataSet: costTableDataSetProps;
    productInfo: productInfoProps[];
}) => {
    // @ts-ignore
    const tableData: costTableDataProps[] = createTableData(costTableDataSet, productInfo);

    // @ts-ignore
    return <DefaultTable data={tableData} columns={productCardColumns} />;
};
