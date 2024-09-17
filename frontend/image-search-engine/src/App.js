import React, { useState } from "react";
import { Search } from "lucide-react";
import ImageUpload from "./components/ImageUpload";
import ImageSearch from "./components/ImageSearch";
import ImageList from "./components/ImageList";

const App = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [isSearchLoading, setIsSearchLoading] = useState(false);
  const [isListLoading, setIsListLoading] = useState(false);

  const handleSearch = async (searchTerm) => {
    setIsSearchLoading(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    // Your actual search logic here
    setIsSearchLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-indigo-700 mb-4">Image Search Engine</h1>
          <ImageSearch
            setSearchResults={setSearchResults}
            onSearch={handleSearch}
            isLoading={isSearchLoading}
          />
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <section className="mb-12">
          <ImageUpload setUploadedImage={setUploadedImage} />
        </section>

        <section className="bg-white shadow-xl rounded-lg p-8">
          <h2 className="text-2xl font-semibold mb-6">Search Results</h2>
          {isSearchLoading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-indigo-500"></div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                {searchResults && searchResults.map((image, index) => {
                const url = image.image_url;
                const params = new URLSearchParams(new URL(url).search);
                const fileId = params.get('id');

                return (
                  <div key={index} className="image-card bg-white border border-gray-200 rounded-lg overflow-hidden shadow-lg transition-all duration-300 hover:shadow-2xl hover:-translate-y-1">
                    <img
                      src={`https://drive.google.com/thumbnail?id=${fileId}`}
                      alt={image.description}
                      className="w-full h-96 object-cover"
                    />
                    <div className="p-4">
                      <p className="text-sm font-medium text-gray-700">{image.description}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </section>

        <section className="mt-12">
          <h2 className="text-2xl font-semibold mb-6">All Images</h2>
          <ImageList isLoading={isListLoading} setIsLoading={setIsListLoading} />
        </section>
      </main>
    </div>
  );
};

export default App;