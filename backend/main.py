import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database import create_table, insert_image_data
from google_drive import upload_to_google_drive
from openai_utils import generate_image_description, generate_vector

load_dotenv()  # Load environment variables

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Adjust this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await create_table()


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(await file.read())
            tmp_file.flush()
            file_path = tmp_file.name

        # Upload image to Google Drive
        image_url = await upload_to_google_drive(file_path)

        # Generate description from OpenAI
        print('generate image description')
        description = await generate_image_description(file_path)
        print("end generate image description")

        # Generate vector from the description
        vector_data = await generate_vector(description)

        # Insert data into PostgreSQL
        await insert_image_data(image_url, description, vector_data)

        # Clean up the temporary file
        os.remove(file_path)

        return {"status": "success", "image_url": image_url, "description": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
