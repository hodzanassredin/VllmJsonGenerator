import requests
import json

def generate_qa_pairs(system, text, endpoint, model_name, use_json = False, json_schema = None):
    url = endpoint  # URL для API OpenAI
    headers = {
        #"Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_name,  # Используем указанную модель
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": text}
        ],
        'temperature': 0.4,
        'frequency_penalty': 0.0,
        'max_tokens': 2048,
        'top_p': 0.8
    }
    if use_json:
        if json_schema is not None:
            data["response_format"] = {
                "type": "json_schema",
                "json_schema": json_schema
            }
        else:
            data["response_format"] = {"type": "json_object"}
    print(f'requesting ulr {url}')
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
    

endpoint = "http://localhost:8099/v1/chat/completions"
model_name =  "/models/Cotype-Nano-8bit.gguf"
system = '''
Read the following documentation and generate as many question-answer pairs as possible based on the information in the text. Provide the result as a JSON array of objects with `question` and `answer` fields.
Escape the quotes.

**Documentation:**

Python is a general-purpose, high-level programming language. It was created by Guido van Rossum and first released in 1991. Python supports several programming paradigms, including object-oriented, imperative, and functional programming. It is known for its simplicity and readability. Simple python program

print("Hello world.")

**Output format:**
[
{"question": "What is Python?", "answer": "Python is a high-level, general-purpose programming language."},
{"question": "Who created Python?", "answer": "Guido van Rossum"},
{"question": "When was Python first released?", "answer": "In 1991"},
{"question": "What programming paradigms does Python support?", "answer": "Object-oriented, imperative, and functional programming"},
{"question": "What is Python known for?", "answer": "Simplicity and readability of code"},
]
'''

text = '''
Paris (French: Paris IPA: [paˈʁi]о file) is the capital and largest city of France. It is located in the north of the country, in the central part of the Paris Basin, on the Seine River. Population: 2,102,650 (2023)[4][no source]. The center of the Greater Paris agglomeration (6.6 million), the core of the historical region of Île-de-France (more than 12 million)[5]. It forms a commune and a department, divided into 20 arrondissements.

It is considered a global city and world financial center. It is home to the headquarters of UNESCO and a number of other international organizations.

The historic center, formed by the Ile de la Cité and both banks of the Seine, developed over the centuries. In the second half of the 19th century, it underwent a radical reconstruction. The palace and park ensemble of Versailles is located in the suburbs.

Founded in the 3rd century BC. Celtic tribe of Parisii. From the 3rd-4th centuries it was known as the Gallo-Roman city of Parisii. Since the end of the 10th century, with interruptions, it has been the capital of France.
'''

json_schema = {
                    "name": "qa_response",
                    "strict": True,
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "question": {
                                    "type": "string",
                                    "minLength": 10,
                                    "maxLength": 1024
                                },
                                "answer": {
                                    "type": "string",
                                    "minLength": 10,
                                    "maxLength": 1024
                                }
                            },
                            "required": ["question", "answer"],
                            "additionalProperties": False
                        },
                        "minItems": 10,
                        "maxItems": 100
                    }
                }

def get_json(myjson):
  try:
    return json.loads(myjson)
  except ValueError as e:
    return None

def print_res(res):
   obj = get_json(res)
   
   if obj is not None and isinstance(obj, list):
      print(json.dumps(obj, indent=4, ensure_ascii=False))
      print(f"VALID, len {len(obj)}")
   else:
      print(res)
      print("INVALID")


print("================================ NO JSON ========================================")
print_res(generate_qa_pairs(system, text, endpoint, model_name, use_json = False)['choices'][0]['message']['content'])
print("================================    JSON ========================================")
print_res(generate_qa_pairs(system, text, endpoint, model_name, use_json = True)['choices'][0]['message']['content'])
print("================================    JSON SCHEMA =================================")
print_res(generate_qa_pairs(system, text, endpoint, model_name, use_json = True, json_schema = json_schema)['choices'][0]['message']['content'])
