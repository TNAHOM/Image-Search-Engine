import os
import asyncpg
from dotenv import load_dotenv
# from pgvector.asyncpg import register_vector
from DB.psycopg2_connection import get_connection

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


async def create_table():
    conn = await get_connection()

    # Ensure the pgvector extension is enabled
    await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Drop the existing table if it exists and create a new one
    await conn.execute(
        """
        DROP TABLE IF EXISTS items;
        CREATE TABLE items (
            id SERIAL PRIMARY KEY,
            image_url TEXT NOT NULL,          -- Store the image URL
            description TEXT NOT NULL,        -- Store the description of the image
            embedding vector(1536)             -- Store the vectorized description (embedding)
        );
        """
    )

    # Add an index on the embedding for efficient querying (using HNSW)
    await conn.execute("CREATE INDEX ON items USING hnsw (embedding vector_l2_ops);")

    await conn.close()

async def insert_image_data(image_url: str, description: str, embedding):
    conn = await get_connection()
    try:
        # Insert image URL, description, and vectorized embedding
        await conn.execute(
            """
            INSERT INTO items (image_url, description, embedding)
            VALUES ($1, $2, $3)
            """,
            image_url,
            description,
            embedding,  # Embedding as a list (asyncpg handles the vector type)
        )
    finally:
        await conn.close()
