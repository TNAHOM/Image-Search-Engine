import os
import asyncpg
from dotenv import load_dotenv
from pgvector.asyncpg import register_vector

# Load environment variables from .env file
load_dotenv()

DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]


async def get_connection() -> asyncpg.Connection:
    try:
        conn = await asyncpg.connect(
            database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST
        )
        await register_vector(conn)  # Ensure to await the coroutine
        return conn
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        raise



async def create_table() -> None:
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
