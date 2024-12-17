import os
from mistralai import Mistral
from skfin.datasets import load_fomc_statements
import tqdm 

with open("../mistral_key.txt", "r") as f:
    api_key = f.read().strip()
def analyze_monetary_policy_hawkishness(api_key, statements):
    model = "mistral-large-latest"
    client = Mistral(api_key=api_key)

    results = []

    for text in statements:
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"Act as a financial analyst. What is the monetary policy hawkishness of this text? \
    Please choose an answer from hawkish, dovish, neutral or unknown and provide a probability and a short explanation. \
        answer in this structure (no other text) : \n \
        label: hawkish, \n probability: 90%, \n explanation: The text contains a lot of positive words and is likely to be hawkish. \n \
    Text: {text}",
                },
            ]
        )

        response_message = chat_response.choices[0].message.content
        # Assuming the response message contains the label and probability in a specific format
        # You may need to adjust the parsing based on the actual response format
        # label = response_message.split(':')[1].split(',')[0].strip()
        # probability = response_message.split('probability')[1].split('%')[0].strip()

        results.append({ "text": response_message})

    return results

statements = load_fomc_statements(force_reload=False, cache_dir="../nbs/data")

# Example usage:
""
# print(len(statements))

results = analyze_monetary_policy_hawkishness(api_key, statements)
for i,result in enumerate(results):
    print(f" i: {i} \n {result['text']} \n")
    print('---'*20)