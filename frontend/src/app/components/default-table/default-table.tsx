import {
    Column,
    Table,
    flexRender,
    useReactTable,
    getCoreRowModel,
    getFilteredRowModel,
    getPaginationRowModel,
    ColumnDef,
    getSortedRowModel,
    ColumnFiltersState,
    SortingState,
} from "@tanstack/react-table";
import "./table.css";
import Pagination from "./default-pagination";
import { useState, InputHTMLAttributes, useEffect } from "react";

interface TableDataProps<TData> {
    data: TData[];
    columns: ColumnDef<TData>[];
}
interface tableProps<TData> {
    table: Table<TData>;
}

// A debounced input react component
function DebouncedInput({
    value: initialValue,
    onChange,
    debounce = 500,
    ...props
}: {
    value: string | number;
    onChange: (value: string | number) => void;
    debounce?: number;
} & Omit<InputHTMLAttributes<HTMLInputElement>, "onChange">) {
    const [value, setValue] = useState(initialValue);

    useEffect(() => {
        setValue(initialValue);
    }, [initialValue]);

    useEffect(() => {
        const timeout = setTimeout(() => {
            onChange(value);
        }, debounce);

        return () => clearTimeout(timeout);
    }, [value]);

    return <input {...props} value={value} onChange={(e) => setValue(e.target.value)} />;
}

function ColumnFiltering({ column, table }: { column: Column<any, unknown>; table: Table<any> }) {
    const columnFilterValue = column.getFilterValue();

    return (
        <div>
            <DebouncedInput
                type="text"
                value={(columnFilterValue ?? "") as string}
                onChange={(value) => column.setFilterValue(value)}
                placeholder={`검색하기`}
                className="w-36 border shadow rounded"
                list={column.id + "list"}
            />
        </div>
    );
}

export const BasicTable = ({ table }: tableProps<any>) => {
    return (
        <table>
            <thead>
                {table.getHeaderGroups().map((headerGroup) => (
                    <tr key={headerGroup.id}>
                        {headerGroup.headers.map((header) => (
                            <th
                                key={header.id}
                                className="text-sm py-2 px-4 sticky top-8 whitespace-nowrap bg-blue-100 z-10">
                                {header.isPlaceholder ? null : (
                                    <>
                                        <div
                                            {...{
                                                className: header.column.getCanSort()
                                                    ? "cursor-pointer select-none"
                                                    : "",
                                                onClick: header.column.getToggleSortingHandler(),
                                            }}>
                                            <>
                                                {flexRender(header.column.columnDef.header, header.getContext())}
                                                {{
                                                    asc: " 🔼",
                                                    desc: " 🔽",
                                                }[header.column.getIsSorted() as string] ?? null}
                                            </>
                                        </div>
                                        {header.column.getCanFilter() ? (
                                            <div>
                                                <ColumnFiltering column={header.column} table={table} />
                                            </div>
                                        ) : null}
                                    </>
                                )}
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

export const TableData = ({ data, columns }: TableDataProps<any>) => {
    useEffect(() => {
        setNewData(data);
    }, [data]);

    const [newData, setNewData] = useState(data);
    const [sorting, setSorting] = useState<SortingState>([]);
    const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
    return useReactTable({
        data: newData,
        columns,
        getCoreRowModel: getCoreRowModel(),
        getPaginationRowModel: getPaginationRowModel(),
        getSortedRowModel: getSortedRowModel(),
        getFilteredRowModel: getFilteredRowModel(),
        state: {
            sorting,
            columnFilters,
        },
        meta: {
            updateData: (rowIndex: any, columnId: any, value: any) => {
                // Skip page index reset until after next rerender
                setNewData((old) =>
                    old.map((row, index) => {
                        if (index === rowIndex) {
                            return {
                                ...old[rowIndex],
                                [columnId]: value,
                            };
                        }
                        return row;
                    })
                );
            },
        },
        onColumnFiltersChange: setColumnFilters,
        onSortingChange: setSorting,
        initialState: {
            pagination: {
                pageSize: 50,
            },
        },
    });
};

const DefaultTable = ({ data, columns }: TableDataProps<any>) => {
    const table = TableData({ data, columns });
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
