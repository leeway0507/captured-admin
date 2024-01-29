"use client";
import { toast } from "react-toastify";
import { uploadThumbnail, updateThumbnailMeta, updateImageToS3 } from "../fetch";
import BaseModal from "@/app/dev/tables/candidate/modal/modal";
import { useState } from "react";

export const ThumbnailUploadBtn = () => {
    const Handler = () => {
        uploadThumbnail().then((res) =>
            res.status == 200 ? toast.success("썸네일 업로드 성공") : toast.error("네트워크 오류 발생")
        );
    };
    return (
        <button onClick={Handler} className="px-3 py-2 bg-gray-200 rounded border">
            썸네일 업로드
        </button>
    );
};

export const ThumbnailMetaUpdateBtn = () => {
    const Handler = () => {
        updateThumbnailMeta().then((res) =>
            res.status == 200 ? toast.success("썸네일 메타데이터 업데이트") : toast.error("네트워크 오류 발생")
        );
    };
    return (
        <button onClick={Handler} className="px-3 py-2 bg-gray-200 rounded border">
            썸네일 메타 업데이트
        </button>
    );
};

export const ImageUploadBtn = () => {
    const [sku, setSku] = useState<number>();
    const [fileName, setFileName] = useState<string>();
    const [isOpen, setIsOpen] = useState<boolean>(false);

    const Handler = () => {
        updateImageToS3(sku!, fileName!).then((res) =>
            res.status == 200 ? toast.success("썸네일 메타데이터 업데이트") : toast.error("네트워크 오류 발생")
        );
    };
    const content = (
        <>
            <div>
                <div>SKU</div>
                <input
                    type="text"
                    className="border border-black h-[30px]"
                    onChange={(e) => setSku(Number(e.target.value))}
                />
            </div>
            <div>
                <div>file_name</div>
                <input
                    type="text"
                    className="border border-black h-[30px]"
                    onChange={(e) => setFileName(e.target.value)}
                />
            </div>
            <button onClick={Handler} className="my-2 px-3 py-2 bg-gray-200 rounded border">
                업로드
            </button>
        </>
    );
    const closeModal = () => setIsOpen(false);
    const openModal = () => setIsOpen(true);

    return (
        <>
            <button onClick={openModal} className="px-3 py-2 bg-gray-200 rounded border">
                이미지 업데이트
            </button>

            {BaseModal({
                content: content,
                isOpen: isOpen,
                closeModal: closeModal,
            })}
        </>
    );
};
