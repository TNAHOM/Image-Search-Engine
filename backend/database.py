import os
import asyncpg
from dotenv import load_dotenv
# from pgvector.asyncpg import register_vector
from DB.psycopg2_connection import get_connection

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


async def create_table():
    conn = await get_connection()
    try:
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")

        # Check if the table already exists
        table_exists = await conn.fetchval(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'items')"
        )

        if not table_exists:
            await conn.execute(
                """
                CREATE TABLE items (
                    id bigserial PRIMARY KEY,
                    image_url text NOT NULL,
                    description text NOT NULL,
                    embedding vector(1536)
                )
                """
            )
            await conn.execute(
                "CREATE INDEX ON items USING hnsw (embedding vector_l2_ops)"
            )
            print("Table 'items' created successfully.")
        else:
            print("Table 'items' already exists. Skipping creation.")
    except Exception as e:
        print(f"Error during table creation: {e}")
        raise
    finally:
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
