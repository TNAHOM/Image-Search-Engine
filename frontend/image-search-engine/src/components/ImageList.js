import React, { useEffect, useState } from "react";
import { fetchImages } from "../api";
import { ImageOff } from "lucide-react";

const ImageList = () => {
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadImages = async () => {
            try {
                setLoading(true);
                const imagesList = await fetchImages();
                if (imagesList) {
                    setImages(imagesList);
                } else {
                    setError("Failed to load images");
                }
            } catch (err) {
                setError("An error occurred while fetching images");
            } finally {
                setLoading(false);
            }
        };

        loadImages();
    }, []);

    const handleImageError = (event, fileId) => {
        event.target.src = `https://drive.google.com/thumbnail?id=${fileId}&retry=1`;
    };

    const handleImageLoad = (event) => {
        event.target.classList.remove("opacity-0");
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-indigo-500"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-center text-red-500 py-8">
                <ImageOff className="mx-auto mb-4" size={48} />
                <p className="text-xl font-semibold">{error}</p>
            </div>
        );
    }

    if (!images || images.length === 0) {
        return (
            <div className="text-center text-gray-500 py-8">
                <ImageOff className="mx-auto mb-4" size={48} />
                <p className="text-xl font-semibold">No images found.</p>
            </div>
        );
    }

    return (
        <div className="image-list">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">Uploaded Images</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {images.map((image, index) => {
                    const url = image.image_url;
                    const params = new URLSearchParams(new URL(url).search);
                    const fileId = params.get('id');
                    console.log(`https://drive.google.com/thumbnail?id=${fileId}`, '--+++++')

                    return (
                        <div key={index} className="image-card bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
                            <div className="aspect-w-16 aspect-h-9 bg-gray-100">
                                
                                <img
                                    src={`https://drive.google.com/thumbnail?id=${fileId}`}
                                    alt={image.description}
                                    className="w-full h-full object-cover transition-opacity duration-300 opacity-0"
                                    loading="lazy"
                                    onLoad={handleImageLoad}
                                    onError={(e) => handleImageError(e, fileId)}
                                />
                            </div>
                            <div className="p-4">
                                <p className="text-sm text-gray-600 line-clamp-2">{image.description}</p>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default ImageList;