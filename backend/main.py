import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from DB.psycopg2_connection import create_table, get_connection
from database import insert_image_data
from google_drive import upload_to_google_drive
from openai_utils import generate_image_description, generate_vector
from updated_query import llm_query
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # Load environment variables

app = FastAPI()
origins = ["http://localhost:3000"]
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust this to your frontend URL
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
        print("Generating image description...")
        description = await generate_image_description(file_path)
        print("Image description generated.")

        # Generate vector from the description
        vector_data = await generate_vector(description)

        # Insert data into PostgreSQL
        await insert_image_data(image_url, description, vector_data)

        # Clean up the temporary file
        os.remove(file_path)

        return {"status": "success", "image_url": image_url, "description": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def text_to_vector_search(query_text: str, threshold=0.6):
    # Update the search query using LLMs
    update_text = llm_query(query_text)
    if update_text == "nothing":
        return "nothing"

    query_embedding = await generate_vector(update_text)

    # Establish an asyncpg connection
    conn = await get_connection()

    operator = "<=>"  # Distance operator for vector similarity (Euclidean distance)

    # Perform the query using asyncpg's `fetch` method
    query = f"""
        SELECT id, image_url, description, (embedding {operator} $1) AS score
        FROM items
        WHERE (embedding {operator} $1) >= $2
        ORDER BY score ASC;
    """

    # Use asyncpg's `fetch` method to run the query
    results = await conn.fetch(query, query_embedding, threshold)

    await conn.close()  # Ensure to close the connection

    # Print all results
    for x in results:
        print(x)

    return results


@app.get("/search/")
async def search_images(query_text: str = Query(..., description="Text to search by")):
    try:
        results = await text_to_vector_search(query_text)
        if not results or results == "nothing":
            return {"status": "no results", "results": []}
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/images/")
async def list_images():
    try:
        conn = await get_connection()
        query = "SELECT image_url, description FROM items;"
        results = await conn.fetch(query)
        await conn.close()
        return {"images": results}
    except Exception as e:
        print(f"Error in /images/ endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
