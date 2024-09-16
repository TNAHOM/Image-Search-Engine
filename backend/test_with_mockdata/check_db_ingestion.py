import asyncio
import random
from ..database import insert_image_data
from ..openai_utils import generate_vector


# Function to generate random embeddings (256-dimensional vector)
async def generate_random_embedding(description, dim=256):
    # Await the asynchronous generate_vector function to get the embedding
    return await generate_vector(description)


async def test_insert_image_data():

    # Insert random data
    for i in range(5):  # Insert 5 random rows
        image_url = f"https://example.com/image{i}.jpg"
        description = f"Description of image {i}"
        embedding = await generate_random_embedding(description=description)

        await insert_image_data(image_url, description, embedding)

    print("Test data inserted successfully!")


# Entry point to run the asynchronous test function
if __name__ == "__main__":
    asyncio.run(test_insert_image_data())
