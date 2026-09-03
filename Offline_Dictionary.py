import requests

#Typing in a word will show the complete definition along with synonyms and antonyms. You can select synonyms/antonyms in order to view definition of those along wth more
#synonyms/antonyms.

def get_thesaurus():
  url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/umpire?key=2e315893-3873-4d30-87ca-76c03247fbc0"
  response = requests.get(url)
  data = response.json()
  entry = data[0]

  if response.status_code == 200:
    data = response.json() #data is a list
    wordToBeDefined = data[0]["hwi"]["hw"]#hwi is headword info, hw is headword string
    wordType = data[0]["fl"]
    wordDefinitions = [] #def is a list of definitions for the given word. Lists are denoted by brackets (index by number). Curly braces are dicitionaries (index by name)
    for sseq in entry["def"][0]["sseq"]:
      for sense in sseq: #iterate through the list of senses (meanings) for a given word. For each sense in the list of sense sequences, do x
        sense_data = sense[1] #skip to 1, as sense[0] is just "sense"
        if "dt" in sense_data: #if "defining text" is in the sense data of a particular, listed sense
          for dt_item in sense_data["dt"]: #append the definition text to the list of defining text
            if dt_item[0] == "text":
              wordDefinitions.append(dt_item[1])

    return wordToBeDefined, wordType, wordDefinitions
  else: 
    return None

defineThis = get_thesaurus()
if defineThis is not None: 
  print(f"{defineThis}")
else:
  print("Did not work properly.")




#ctrl + / com,ment out multiple lines