export const getCursor = async (page: string | number) => {
    const req = await fetch(`http://127.0.0.1:8000/api/admin/get-cursor-test?page=${page}`);
    return await req.json();
};
