import React, { useState } from "react";
import { Search } from "lucide-react";
import axios from "axios";

const ImageSearch = ({ setSearchResults, onSearch, isLoading }) => {
    const [queryText, setQueryText] = useState("");
    const [error, setError] = useState(null);

    const handleSearch = async (e) => {
        e.preventDefault();
        onSearch(queryText);
        try {
            const response = await axios.get("http://localhost:8000/search/", {
                params: { query_text: queryText },
            });

            if (response.data.results.length === 0) {
                alert("No results found.");
            }
            setSearchResults(response.data.results);
            setError(null); // Reset any previous errors
        } catch (error) {
            console.error("Error searching images:", error);
            setError("Failed to search images. Please try again.");
        }
    };

    return (
        <div>
            <form onSubmit={handleSearch} className="relative">
                <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Search for images..."
                    className="w-full py-3 px-4 pr-12 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                />
                <button
                    type="submit"
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-indigo-500 focus:outline-none"
                    disabled={isLoading}
                >
                    {isLoading ? (
                        <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-indigo-500"></div>
                    ) : (
                        <Search size={20} />
                    )}
                </button>
            </form>

            {/* Show error message if search fails */}
            {error && (
                <div className="mt-2 text-red-600">
                    <p>{error}</p>
                </div>
            )}
        </div>
    );
};

export default ImageSearch;
