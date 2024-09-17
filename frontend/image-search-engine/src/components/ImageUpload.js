import React, { useState, useRef } from "react";
import axios from "axios";
import { Upload, X, CheckCircle, AlertCircle } from "lucide-react";

const ImageUpload = ({ setUploadedImage }) => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState(null);
    const [isDragActive, setIsDragActive] = useState(false);
    const fileInputRef = useRef(null);

    const handleFile = (selectedFile) => {
        setFile(selectedFile);
        setPreview(URL.createObjectURL(selectedFile));
    };

    const handleDragEnter = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        setUploading(true);
        setUploadStatus(null);

        try {
            const response = await axios.post("http://localhost:8000/upload/", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            setUploadedImage(response.data.image_url);
            setUploadStatus("success");
        } catch (error) {
            console.error("Error uploading image:", error);
            setUploadStatus("error");
        } finally {
            setUploading(false);
        }
    };

    const resetUpload = () => {
        setFile(null);
        setPreview(null);
        setUploadStatus(null);
    };

    return (
        <div className="mb-8">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">Upload Image</h2>
            <div
                onDragEnter={handleDragEnter}
                onDragLeave={handleDragLeave}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current.click()}
                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${isDragActive ? "border-indigo-500 bg-indigo-50" : "border-gray-300 hover:border-indigo-400"
                    }`}
            >
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleChange}
                    accept="image/*"
                    className="hidden"
                />
                {preview ? (
                    <div className="relative">
                        <img src={preview} alt="Preview" className="max-h-48 mx-auto rounded-md" />
                        <button
                            onClick={(e) => { e.stopPropagation(); resetUpload(); }}
                            className="absolute top-0 right-0 bg-red-500 text-white p-1 rounded-full hover:bg-red-600 transition-colors"
                        >
                            <X size={16} />
                        </button>
                    </div>
                ) : (
                    <div className="text-gray-500">
                        <Upload className="mx-auto mb-4" size={48} />
                        <p className="text-lg font-semibold">
                            {isDragActive ? "Drop the image here" : "Drag 'n' drop an image here, or click to select"}
                        </p>
                    </div>
                )}
            </div>
            {file && (
                <div className="mt-4 flex justify-center">
                    <button
                        onClick={handleUpload}
                        disabled={uploading}
                        className={`px-6 py-2 rounded-full text-white font-semibold transition-colors ${uploading ? "bg-gray-400 cursor-not-allowed" : "bg-indigo-500 hover:bg-indigo-600"
                            }`}
                    >
                        {uploading ? "Uploading..." : "Upload Image"}
                    </button>
                </div>
            )}
            {uploadStatus && (
                <div className={`mt-4 text-center font-semibold ${uploadStatus === "success" ? "text-green-500" : "text-red-500"
                    }`}>
                    {uploadStatus === "success" ? (
                        <p className="flex items-center justify-center">
                            <CheckCircle className="mr-2" size={20} />
                            Image uploaded successfully!
                        </p>
                    ) : (
                        <p className="flex items-center justify-center">
                            <AlertCircle className="mr-2" size={20} />
                            Failed to upload image. Please try again.
                        </p>
                    )}
                </div>
            )}
        </div>
    );
};

export default ImageUpload;