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
Прочитай следующую документацию и сгенерируй максимальное количество пар вопрос-ответ на основе информации из текста. Представь результат в формате JSON массива с обьектами с полями `question` и `answer`.
Экранируй кавычки.

**Документация:**

Python — это высокоуровневый язык программирования общего назначения. Он был создан Гвидо ван Россумом и впервые выпущен в 1991 году. Python поддерживает несколько парадигм программирования, включая объектно-ориентированное, императивное и функциональное программирование. Он известен своей простотой и читаемостью кода.
Простая программа на python

print("Hello world.") 

**Формат вывода:**
[
{"question": "Что такое Python?", "answer": "Python — это высокоуровневый язык программирования общего назначения."},
{"question": "Кто создал Python?", "answer": "Гвидо ван Россум"},
{"question": "Когда был впервые выпущен Python?", "answer": "В 1991 году"},
{"question": "Какие парадигмы программирования поддерживает Python?", "answer": "Объектно-ориентированное, императивное и функциональное программирование"},
{"question": "Чем известен Python?", "answer": "Простотой и читаемостью кода"},
]
'''

text = '''
Пари́ж (фр. Paris МФА: [paˈʁi]о файле) — столица и крупнейший город Франции. Находится на севере государства, в центральной части Парижского бассейна, на реке Сена. Население — 2 102 650 человек (2023)[4][нет в источнике]. Центр агломерации Большой Париж (6,6 млн), ядро исторического региона Иль-де-Франс (более 12 млн)[5]. Образует коммуну и департамент, разделённый на 20 округов.

Относится к глобальным городам и мировым финансовым центрам. Здесь располагаются штаб-квартиры ЮНЕСКО и ряда других международных организаций.

Исторический центр, образованный островом Сите и обоими берегами Сены, складывался на протяжении веков. Во второй половине XIX века претерпел коренную реконструкцию. В пригороде расположен дворцово-парковый ансамбль Версаль.

Основан в III веке до н. э. кельтским племенем паризиев. С III—IV веков известен как галло-римский город Паризии. С конца X века с перерывами является столицей Франции. 
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
