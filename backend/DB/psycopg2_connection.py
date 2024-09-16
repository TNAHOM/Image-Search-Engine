import os
import numpy as np
import psycopg2
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector

# Load environment variables from .env file
load_dotenv(override=True)
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
# DBSSL = "disable" if DBHOST == "localhost" else "require"

# Establish connection to PostgreSQL
conn = psycopg2.connect(
    database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST
)
conn.autocommit = True
cur = conn.cursor()

# Ensure the pgvector extension is enabled
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

# Drop the existing table if it exists and create a new one
cur.execute("DROP TABLE IF EXISTS items")
cur.execute(
    """
    CREATE TABLE items (
        id bigserial PRIMARY KEY,
        image_url text NOT NULL,              -- Store the image URL
        description text NOT NULL,            -- Store the description of the image
        embedding vector(1536)                   -- Store the vectorized description (embedding)
    )
"""
)

# Register pgvector for this connection
register_vector(conn)

# Add an index on the embedding for efficient querying (using HNSW)
cur.execute("CREATE INDEX ON items USING hnsw (embedding vector_l2_ops)")

# Close the cursor and connection
cur.close()
conn.close()
