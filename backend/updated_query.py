import os
from openai import OpenAI

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

systemPrompt = """
Describe the text in color, type of cloth if its a tshirt pants or an other,  Embellishment, Pattern or Design, and overall what the query text express in terms of cloth. If their is no nothing that it could express a cloth just ignore it and output 'nothing'.

"""


client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def llm_query(query_search):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": systemPrompt,
            },
            {
                "role": "user",
                "content": query_search,
            },
        ],
        model=model_name,
        temperature=0.3,
        max_tokens=50,
    )

    output = response.choices[0].message.content
    print(output, "query_search")
    return output
