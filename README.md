# Image Search Engine

## Description

This project is a modern web application that allows users to upload images, search through them, and view the results in an elegant interface. It features a responsive design, drag-and-drop image upload functionality, and a powerful search capability using vector embeddings for enhanced accuracy.

## Features

- Image upload with drag-and-drop support
- Image search functionality using vector embeddings
- Responsive grid layout for displaying search results
- Modern UI with smooth animations and transitions
- Integration with Google Drive for image storage
- Utilization of OpenAI's embeddings models for advanced search capabilities

## Technology Stack

- Frontend: React.js with Tailwind CSS for styling
- Backend: FastAPI with PostgreSQL and pgvector
- Image Storage: Google Drive
- Vector Embeddings: OpenAI embeddings models
- API: RESTful API for image upload and search

## Installation

### Prerequisites

- Node.js and npm
- Python 3.7+
- PostgreSQL with pgvector extension
- Google Drive API credentials

### Frontend Setup

1. Clone the repository:

   ```
   git clone https://github.com/TNAHOM/Image-Search-Engine.git
   cd Image-Search-Engine/frontend
   ```

2. Install dependencies:

   ```
   npm install
   ```

3. Create a `.env` file in the frontend directory and add necessary environment variables:

   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```
   npm start
   ```

### Backend Setup

1. Navigate to the backend directory:

   ```
   cd ../backend
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install required packages:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory and add necessary environment variables:

   ```
   DATABASE_URL=postgresql://username:password@localhost/dbname
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_DRIVE_CREDENTIALS_FILE=path/to/your/credentials.json
   ```

5. Set up the database:

   ```
   alembic upgrade head
   ```

6. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

## Usage

1. **Uploading Images:**

   - Drag and drop an image into the upload area, or click to select a file.
   - Click the "Upload Image" button to submit the image.

2. **Searching Images:**

   - Use the search bar at the top of the page to enter your search query.
   - Press Enter or click the search button to view results.

3. **Viewing Results:**
   - Scroll through the responsive grid of image results.
   - Click on an image to view it in full size (if implemented).

## API Endpoints

- `/upload/`: POST request to upload an image
- `/search/`: GET request to search for images using vector embeddings

For detailed API documentation, run the backend server and visit `http://localhost:8000/docs`.

## Contributing

Contributions to the Image Search Engine project are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request

Please ensure your code adheres to the project's coding standards and include tests for new features.

## License

This project is licensed under the MIT License.

## Contact

For any inquiries or issues, please open an issue on the [GitHub repository](https://github.com/TNAHOM/Image-Search-Engine/issues).
