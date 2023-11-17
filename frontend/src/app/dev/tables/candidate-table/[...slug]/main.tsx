import { candidateTableRawDataProps, CandidateTable } from "./table/candidate-table";
import { getBuyingCurrency } from "./fetch";

export interface productCardProps {
    shopProductCardId: number;
    shopProductName: string;
    shopProductImgUrl: string;
    productUrl: string;
    shopName: string;
    brandName: string;
    productId: string;
    korPrice: number;
    usPrice: number;
    originalPriceCurrency: string;
    originalPrice: number;
    soldOut: boolean;
    candidate: number;
    updatedAt: Date;
    coupon: number;
}

export interface shopInfoProps {
    shopName: string;
    shopUrl: string;
    taxReductionRate: number;
    delAgcTaxReductionRate: number;
    domeShipPrice: number;
    intlShipPrice: number;
    fromUsShipping: boolean;
    isDdp: boolean;
    updatedAt: Date;
    country: string;
}

const roundUpTwo = (num: number) => {
    return Math.round(num * 100) / 100;
};

const createTableData = async (productCardList: productCardProps[], shopInfo: shopInfoProps) => {
    const buyingCurrency = await getBuyingCurrency().then((res) => res.data);

    const errorRate = 1.025;
    const cardRate = 0.03;
    const VATRate = 0.1;
    const customRate = 0.13;

    const currencyRate = buyingCurrency["data"][productCardList[0].originalPriceCurrency] * errorRate;

    const usCurrencyRate = buyingCurrency["data"]["USD"];
    const intlShipKorPrice = shopInfo.intlShipPrice * currencyRate;

    function calcCustomAndVAT(usPrice: number, korPrice: number, intlShipKorPrice: number) {
        if (usPrice < 150) return [0, 0];
        if (usPrice < 200 && shopInfo.fromUsShipping) return [0, 0];
        if (shopInfo.isDdp) return [0, 0];

        const customFee = (korPrice + intlShipKorPrice) * customRate;
        const VATFee = (korPrice + intlShipKorPrice + customFee) * VATRate;
        return [customFee, VATFee];
    }

    const result: candidateTableRawDataProps[] = productCardList.map((productCard) => {
        const taxReductionRate = 1 + shopInfo.taxReductionRate;

        const taxReductionOriginalPrice = productCard.originalPrice / taxReductionRate;
        const korPrice = taxReductionOriginalPrice * currencyRate;

        const usPrice = korPrice / usCurrencyRate;
        const [customFee, VATFee] = calcCustomAndVAT(usPrice, korPrice, intlShipKorPrice);

        const totalPriceBeforeCardFee = korPrice + intlShipKorPrice + customFee + VATFee;

        const sellPrice10P = (totalPriceBeforeCardFee * 100) / 87;
        const sellPrice20P = (totalPriceBeforeCardFee * 100) / 77;

        const cardFee = Math.round(sellPrice20P * cardRate);

        return {
            shopProductCardId: productCard.shopProductCardId,
            candidate: productCard.candidate,
            productId: productCard.productId,
            shopProductName: productCard.shopProductName,
            shopProductImgUrl: productCard.shopProductImgUrl,
            productUrl: productCard.productUrl,
            brandName: productCard.brandName,
            originalPriceCurrency: productCard.originalPriceCurrency,
            originalPrice: productCard.originalPrice,
            taxReductionOriginalPrice: roundUpTwo(taxReductionOriginalPrice),
            korPrice: Math.round(korPrice),
            intlShipKorPrice: Math.round(intlShipKorPrice),
            intlShipPrice: shopInfo.intlShipPrice,
            usPrice: Math.round(usPrice),
            customFee: Math.round(customFee),
            VATFee: Math.round(VATFee),
            totalPriceBeforeCardFee: Math.round(totalPriceBeforeCardFee),
            totalPrice: Math.round(totalPriceBeforeCardFee + cardFee),
            sellPrice10P: Math.round(sellPrice10P),
            sellPrice20P: Math.round(sellPrice20P),
            cardFee: cardFee,
            updatedAt: productCard.updatedAt,
        };
    });
    return result;
};

const Main = async ({
    shopInfo,
    productCardList,
}: {
    shopInfo: shopInfoProps;
    productCardList: productCardProps[];
}) => {
    const tableData = await createTableData(productCardList, shopInfo);

    //sort
    tableData.sort((a, b) => a.totalPrice - b.totalPrice);

    return (
        <div className="py-4">
            <CandidateTable tableData={tableData} />
        </div>
    );
};

export default Main;
