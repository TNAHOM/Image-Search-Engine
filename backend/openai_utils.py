import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
import json
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential

from from_json_to_string import convert_json_to_string

# Initialize the Azure EmbeddingsClient
endpoint = "https://models.inference.ai.azure.com"
model_name = "text-embedding-3-small"
token = os.environ["GITHUB_TOKEN"]

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

load_dotenv()


# You are a helpfull clothier that will let users describe their only the cloth from the image based color, Embellishment of the cloth, Pattern or Design, Includes any noticeable structural features that define the garment's overall silhouette and aesthetic.
systemPrompt = """
You are a helpfull clothier that will let users list the keywords of the feature and type of the cloth(if its tshirt or dress, shirt, pants or etc...) from the image based color, Embellishment of the cloth, Pattern or Design, Includes any noticeable structureal feature or specific type of the cloth. 
Describe if only that feature or type or any requirments listed before is vissible or can be clearly described. Add to the json fomrat only a keyword or a phrase. But on the Other section describe in 1 line the general or that wasn mentioned about the cloth.
Return the flashcards in the following JSON format:
{
  "description": [
  {
    "color": "list",
    "Type": "list",
    "Embellishment": "list",
    "Pattern_design": "list",
    "structural_feature": "list",
    "other": "str"
    }
    ]
}
"""


def open_image_as_base64(filename):
    with open(filename, "rb") as image_file:
        image_data = image_file.read()
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    return f"data:image/png;base64,{image_base64}"


async def generate_image_description(image_path: str) -> str:
    # print(image_path)
    image_data_url = open_image_as_base64(image_path)

    if not image_data_url:
        return "Error: Could not process image."
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": systemPrompt,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": systemPrompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": open_image_as_base64(
                                "C:\\Users\\PC\\Desktop\\Projects\\Microsoft Hackaton\\Image search engine\\backend\\test_with_mockdata\\dataset\\Male Pose Reference.jpg",
                            ),
                            "detail": "low",
                        },
                    },
                ],
            },
        ],
        model="gpt-4o-mini",
        max_tokens=150,
        temperature=0.4,
    )

    # print(response.choices[0].message.content, '++++++')
    json_data = json.loads(response.choices[0].message.content)
    result = convert_json_to_string(json_data)
    print(result)
    return result


clientEmbed = EmbeddingsClient(endpoint=endpoint, credential=AzureKeyCredential(token))


async def generate_vector(description: str) -> list:
    response = clientEmbed.embed(input=[description], model=model_name)
    
    for item in response.data:
        length = len(item.embedding)
        print(
            f"data[{item.index}]: length={length}, "
            f"[{item.embedding[0]}, {item.embedding[1]}, "
            f"..., {item.embedding[length-2]}, {item.embedding[length-1]}]"
        )
    print(response.usage, response)
    return response.usage
