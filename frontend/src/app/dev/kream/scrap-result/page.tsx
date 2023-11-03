"use client";

export default function Main() {
    const brandName = "adidas";
    const scrapLen = 50;
    const scrapSuccessLen = 40;
    const scrapFailLen = 5;
    const scrapNotStartLen = 5;

    return (
        <>
            <div className="flex flex-col h-full gap-8 w-full max-w-5xl p-8">
                <div className="text-3xl">제품 상세정보 수집결과</div>
                <div className="border p-4 text-xl grid grid-rows-2 gap-2">
                    <div className="grid grid-cols-8 text-2xl">
                        <div>수집 브랜드</div>
                        <div>{brandName}</div>
                    </div>
                    <div className="grid grid-cols-8">
                        <div>계획</div>
                        <div>{scrapLen} 건</div>
                        <div>성공</div>
                        <div>{scrapSuccessLen} 건</div>
                        <div>실패</div>
                        <div>{scrapFailLen} 건</div>
                        <div>미실행</div>
                        <div>{scrapNotStartLen} 건</div>
                    </div>
                </div>
                <div className="text-3xl">수집 실패 목록</div>

                <div className="flex gap-4 max-w-[500px] text-xl">
                    <button className="black-bar p-4 text-xl">실패 목록 재실행</button>
                    <button className="black-bar p-4 text-xl">돌아가기</button>
                </div>
            </div>
        </>
    );
}
