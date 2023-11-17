import {
    Table,
    flexRender,
    useReactTable,
    getCoreRowModel,
    getPaginationRowModel,
    ColumnDef,
    ColumnDefBase,
} from "@tanstack/react-table";
import "./table.css";
import Pagination from "./pagination";

interface TableDataProps<TData> {
    data: TData[];
    columns: ColumnDef<TData>[];
}
interface tableProps<TData> {
    table: Table<TData>;
}

const BasicTable = ({ table }: tableProps<any>) => {
    return (
        <table>
            <thead>
                {table.getHeaderGroups().map((headerGroup) => (
                    <tr key={headerGroup.id}>
                        {headerGroup.headers.map((header) => (
                            <th
                                key={header.id}
                                className="text-sm py-2 px-4 sticky top-8 whitespace-nowrap bg-blue-100 z-10">
                                {header.isPlaceholder
                                    ? null
                                    : flexRender(header.column.columnDef.header, header.getContext())}
                            </th>
                        ))}
                    </tr>
                ))}
            </thead>
            <tbody>
                {table.getRowModel().rows.map((row) => (
                    <tr key={row.id}>
                        {row.getVisibleCells().map((cell) => (
                            <td className="text-xs px-2 " key={cell.id}>
                                {flexRender(cell.column.columnDef.cell, cell.getContext())}
                            </td>
                        ))}
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

const DefaultTable = ({ data, columns }: TableDataProps<any>) => {
    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
        getPaginationRowModel: getPaginationRowModel(),
        initialState: {
            pagination: {
                pageSize: 50,
            },
        },
    });
    return (
        <div className="flex flex-col w-full">
            <div className="sticky top-0 bg-white w-full z-10">
                <Pagination table={table} />
            </div>
            <BasicTable table={table} />
            <div className="py-4">
                <Pagination table={table} />
            </div>
        </div>
    );
};

export default DefaultTable;
