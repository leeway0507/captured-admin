export const getCandidateTable = async (searchType: string, content: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/table/candidate-table`;
    const queryParams = new URLSearchParams({
        searchType,
        content,
    });

    const res = await fetch(url + "?" + queryParams, { cache: "no-cache" });
    return { status: res.status, data: await res.json() };
};

export const updateCandidateCard = async (shopProductCardId: number, value: object) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/table/candidate-table`;
    const body = {
        shopProductCardId,
        value,
    };
    const res = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });
    return { status: res.status, data: await res.json() };
};

export const patchCandidateCard = async (shopProductCardId: number, column: string, content: any) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/table/candidate-table`;
    const queryParams = new URLSearchParams({
        shopProductCardId: shopProductCardId.toString(),
        column,
        content,
    });

    const res = await fetch(url + "?" + queryParams, { method: "PATCH" });
    return { status: res.status, data: await res.json() };
};

export const deleteCandidateCard = async (shopProductCardId: number) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/table/candidate-table/${shopProductCardId}`;

    const res = await fetch(url, {
        method: "DELETE",
    });
    return { status: res.status, data: await res.json() };
};

export const getSizeData = async (productId: string) => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/table/size-table/${productId}`;
    const res = await fetch(url);
    return { status: res.status, data: await res.json() };
};
