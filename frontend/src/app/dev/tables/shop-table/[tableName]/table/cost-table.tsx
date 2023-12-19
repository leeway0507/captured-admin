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
    kreamMatchInfo: boolean;
}

interface costTableDataSetProps {
    shopInfo: shopInfoProps[];
    shopProductInfo: productCardProps[];
    currency: { data: { [key: string]: any }; updatedAt: Date };
    kreamMatchInfo: string[];
    prodProductInfo: productInfoProps[];
}

interface productInfoProps {
    sku: number;
    productId: string;
    shippingFee: number;
    price: number;
}

const createTableData = (costTableDataSet: costTableDataSetProps) => {
    const { shopInfo: shopInfoRaw, shopProductInfo, currency, kreamMatchInfo, prodProductInfo } = costTableDataSet;

    const buyingCurrency = currency.data;
    return shopProductInfo.map((row) => {
        const shopInfo = shopInfoRaw.find((shopInfo) => shopInfo.shopName === row.shopName);
        const product = prodProductInfo.find((prod) => prod.productId === row.productId);
        const isKreamMatch = kreamMatchInfo.includes(row.productId);

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
            kreamMatchInfo: isKreamMatch,
        };
    });
};

export const CostTable = ({ costTableDataSet }: { costTableDataSet: costTableDataSetProps }) => {
    // @ts-ignore
    const tableData: costTableDataProps[] = createTableData(costTableDataSet);
    tableData.reverse();
    // @ts-ignore
    return <DefaultTable data={tableData} columns={productCardColumns} />;
};
