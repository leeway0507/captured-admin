"use client";
import Image from "next/image";
import Link from "next/link";

import { createColumnHelper } from "@tanstack/react-table";
import { productCardProps } from "../tables/legacy-candidate-table/[...slug]/main";

const columnHelper = createColumnHelper<productCardProps>();

export const SizeTableColumn = [
    columnHelper.accessor("shopName", {
        header: "스토어",
    }),
];
