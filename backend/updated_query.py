import os
from openai import OpenAI

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

systemPrompt = """
Describe what the user text wanted to mean, the text in color, type of cloth if its a tshirt pants or an other, Embellishment, for which gender,Pattern or Design. make the output " result as a string dont use any other symbol like * - or #" Dont say unspecified iinstead ignore that phrase and keyword'.

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
