import axios from "axios";

const API_URL = "http://localhost:8000"; // Change this to your FastAPI URL

// Fetch all images// In api.js
export const fetchImages = async () => {
    console.log('Start FetchImage')
    try {
        const response = await axios.get(`${API_URL}/images/`);
        console.log(response, 'response')
        return response.data.images;
    } catch (error) {
        if (error.response) {
            // Server responded with a status other than 2xx
            console.error("Backend returned an error:", error.response.status);
            console.error(error.response.data);
        } else if (error.request) {
            // Request was made but no response received
            console.error("No response received from backend:", error.request);
        } else {
            // Something else happened
            console.error("Error setting up request:", error.message);
        }
    }
};


// Upload an image
export const uploadImage = async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    try {
        const response = await axios.post(`${API_URL}/upload/`, formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });
        return response.data;
    } catch (error) {
        console.error("Error uploading image:", error);
    }
};
