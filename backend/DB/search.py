import asyncio
from backend.DB.psycopg2_connection import get_connection
from backend.openai_utils import generate_vector


async def text_to_vector_search(query_text: str, top_n=5):
    # Generate the embedding for the query text
    query_embedding = await generate_vector(query_text)

    # Establish an asyncpg connection
    conn = await get_connection()

    operator = "<=>"

    # Perform the query using asyncpg's `fetch` method
    query = f"""
        SELECT id, image_url, description, (embedding {operator} $1) AS score
        FROM items
        ORDER BY score ASC
        LIMIT $2;
    """

    # Use asyncpg's `fetch` method to run the query
    results = await conn.fetch(query, query_embedding, top_n)

    await conn.close()  # Ensure to close the connection

    return results


# Run the asynchronous search function
async def main():
    query_text = "purple color"  # Example text query
    results = await text_to_vector_search(query_text, top_n=5)
    for res in results:
        print(res)


# Run the main function in an asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
