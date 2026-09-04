import requests 
import json



url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/umpire?key=2e315893-3873-4d30-87ca-76c03247fbc0"
response = requests.get(url)
data = response.json()

 
print(json.dumps(data[1], indent=2))