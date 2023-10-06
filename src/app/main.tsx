"use client";
import { useState, useEffect, ChangeEvent, MouseEvent } from "react";

export default function Main() {
    const [data, setData] = useState(false);
    useEffect(() => {
        setData(true);
    }, []);

    return <div>{data}</div>;
}
