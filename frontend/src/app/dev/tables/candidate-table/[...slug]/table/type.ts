
export interface candidateTableRawDataProps {
    shopProductCardId: number; 
    candidate: number;
    shopProductName: string;
    shopProductImgUrl: string;
    productId: string;
    productUrl: string;
    brandName: string;
    originalPriceCurrency: string;
    originalPrice: number;
    taxReductionOriginalPrice: number;
    intlShipKorPrice: number;
    intlShipPrice: number;
    korPrice: number;
    usPrice: number;
    customFee: number;
    VATFee: number;
    totalPriceBeforeCardFee: number;
    totalPrice: number;
    sellPrice10P: number;
    sellPrice20P: number;
    cardFee: number;
    updatedAt: Date;
}
