const Pagination = ({ table }: { table: any }) => {
    return (
        <div className="flex items-center gap-2">
            <button
                className="border rounded p-1 disabled:opacity-50"
                onClick={() => table.setPageIndex(0)}
                disabled={!table.getCanPreviousPage()}>
                {"<<"}
            </button>
            <button
                className="border rounded p-1 disabled:opacity-50"
                onClick={() => (table.previousPage(), window.scrollTo(0, 0))}
                disabled={!table.getCanPreviousPage()}>
                {"<"}
            </button>
            <button
                className="border rounded p-1 disabled:opacity-50"
                onClick={() => (table.nextPage(), window.scrollTo(0, 0))}
                disabled={!table.getCanNextPage()}>
                {">"}
            </button>
            <button
                className="border rounded p-1 disabled:opacity-50"
                onClick={() => table.setPageIndex(table.getPageCount() - 1)}
                disabled={!table.getCanNextPage()}>
                {">>"}
            </button>
            <span className="flex items-center gap-1">
                <div>Page</div>
                <strong>
                    {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}
                </strong>
            </span>
            <span className="flex items-center gap-1">
                | Go to page:
                <input
                    type="number"
                    defaultValue={table.getState().pagination.pageIndex + 1}
                    onChange={(e) => {
                        const page = e.target.value ? Number(e.target.value) - 1 : 0;
                        table.setPageIndex(page);
                    }}
                    className="border p-1 rounded w-16"
                />
            </span>
            <select
                value={table.getState().pagination.pageSize}
                onChange={(e) => {
                    table.setPageSize(Number(e.target.value));
                }}>
                {[50, 100, 200].map((pageSize) => (
                    <option key={pageSize} value={pageSize}>
                        Show {pageSize}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default Pagination;
