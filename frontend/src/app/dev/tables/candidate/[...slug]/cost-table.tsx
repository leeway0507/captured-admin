"use client";
import { productCardColumns } from "./header";
import { shopInfoProps } from "@/app/dev/shop/type";
import { productCardProps } from "@/app/types/type";

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
    shopCard: productCardProps[];
    currency: { data: { [key: string]: any }; updatedAt: Date };
    kreamMatch: string[];
    prodCard: productInfoProps[];
}

interface productInfoProps {
    sku: number;
    productId: string;
    shippingFee: number;
    price: number;
}

const createTableData = (costTableDataSet: costTableDataSetProps) => {
    const { shopInfo: shopInfoRaw, shopCard, currency, kreamMatch, prodCard } = costTableDataSet;

    const buyingCurrency = currency.data;
    return shopCard.map((row) => {
        const shopInfo = shopInfoRaw.find((shopInfo) => shopInfo.shopName === row.shopName);
        const product = prodCard.find((prod) => prod.productId === row.productId);
        const isKreamMatch = kreamMatch.includes(row.productId);

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
