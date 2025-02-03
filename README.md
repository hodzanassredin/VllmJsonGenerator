# VllmJsonGenerator

Demo how to use structured output and simple llm scaling in docker compose.

Ready to use local llama.cpp setup for question, answer pairs json generation for sft.

# Setup

Execute 

> ./up-cuda.sh 

or 

> ./up.sh

# Test

Execute 

> ./test-en.sh 

or 

> ./test-ru.sh

Test scripts attempt to force the model to generate QA pairs.

1. without sctructured output
2. with json object structured output
3. with json schema structured output for array, setting fields lengths and count of expected messages

# Output

================================ NO JSON ========================================

requesting ulr http://localhost:8099/v1/chat/completions

     ```json
     [
     {"question": "What is Paris?", "answer": "Paris is the capital and largest city of France, located in the north-central part of the country."},
     {"question": "Who founded Paris?", "answer": "Paris was founded in the 3rd century BC by the Celtic tribe of Parisii."},
     {"question": "What is the historical period of Paris?", "answer": "The historical period of Paris includes the Celtic period, the Gallo-Roman period, and the medieval period."},
     {"question": "What is the population of Paris?", "answer": "The population of Paris is 2,102,650 (as of 2023)."},
     {"question": "What is the current status of Paris?", "answer": "Paris is considered a global city and the world financial center, with several international organizations headquartered there."},
     {"question": "What is the center of Paris known as?", "answer": "The center of Paris, also known as the Île de la Cité, is formed by the Seine River and has been continuously developed over centuries."},
     {"question": "What is the second half of the 19th century known for in Paris?", "answer": "In the second half of the 19th century, Paris underwent a radical reconstruction."},
     {"question": "What is the palace and park ensemble of Versailles located in?", "answer": "The palace and park ensemble of Versailles is located in the suburbs of Paris."},
     {"question": "What is the meaning of 'Paris' in French?", "answer": "Paris is pronounced as [paˈʁi] in French."},
     {"question": "What is the current department of Paris?", "answer": "Paris is currently part of the 20th arrondissement within the Seine-Saint-Denis department."}
     ]
     ```
     INVALID
  
  
================================    JSON ========================================

requesting ulr http://localhost:8099/v1/chat/completions     INVALID(valid json but array)
```json
    {
    "question": "What is Paris?",
    "answer": "Paris is the capital and largest city of France, located in the central part of the Paris Basin on the Seine River. It is considered a global city and world financial center, home to numerous international organizations."    
    }
```


================================    JSON SCHEMA =================================

requesting ulr http://localhost:8099/v1/chat/completions   VALID, len 10
```json
[
    {
        "question": "What is Paris?",
        "answer": "Paris is the capital and largest city of France, located in the central part of the Paris Basin on the Seine River. It is known for its historical significance, being the center of UNESCO and many other international organizations."
    },
    {
        "question": "Who founded Paris?",
        "answer": "Paris was founded in the 3rd century BC by the Celtic tribe of Parisii."
    },
    {
        "question": "What is the historical center of Paris?",
        "answer": "The historic center of Paris consists of the Île de la Cité and both banks of the Seine."
    },
    {
        "question": "When was Paris first established?",
        "answer": "The city was founded in the 3rd century BC."
    },
    {
        "question": "How many arrondissements are in Paris?",
        "answer": "Paris is divided into 20 arrondissements."
    },
    {
        "question": "What is the current population of Paris?",
        "answer": "The population of Paris is 2,102,650 as of 2023."
    },
    {
        "question": "What is Paris known for?",
        "answer": "Paris is known for its historical significance, being the capital of France, a global city, and a world financial center. It also houses numerous international organizations and UNESCO."
    },
    {
        "question": "What is the current status of Paris?",
        "answer": "Paris is considered a global city and is the world's leading financial center."
    },
    {
        "question": "What is the future of Paris?",
        "answer": "The future of Paris includes ongoing restoration and development of its historic center, with the palace and park ensemble of Versailles located in the suburbs."
    },
    {
        "question": "What is the population of Île-de-France?",
        "answer": "Île-de-France, the historical region of Paris, has a population of more than 12 million."
    }
]
```



