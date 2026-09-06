import requests
from urllib.parse import quote
import json
import streamlit as st

st.title("Word lookup")
uiWord = st.text_input("Enter word:  ", "awaiting...")



#Typing in a word will show the complete definition along with synonyms and antonyms. You can select synonyms/antonyms in order to view definition of those along wth more
#synonyms/antonyms.

def get_thesaurus(word):
  encoded_word = quote(word)
  url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{encoded_word}?key=2e315893-3873-4d30-87ca-76c03247fbc0"
  print(url)
  
  try:
    response = requests.get(url)
    response.raise_for_status() #for failing HTTP status codes
    data = response.json()  
  except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")
    return None
  except requests.exception.JSONDecodeError:
    print("Invalid server data.")
    return None
  
  if not data:
    print(f"No results found for '{word}")
    return None

  
  entry = data[0]

  if isinstance(entry, str):
    print(f"'{word}' wasn't found.")
    return None

  if response.status_code == 200:
    data = response.json() #data is a list

  for entry in data:
    if not isinstance(entry, dict):
      continue

    results = []
    wordToBeDefined = data["hwi"]["hw"]#hwi is headword info, hw is headword string
    wordType = data["fl"]
        
    wordDefinitions = [] #def is a list of definitions for the given word. Lists are denoted by brackets (index by number). Curly braces are dicitionaries (index by name)
    wordSynonyms = []
    wordNearSynonyms = []
    wordPhraseSynonyms = []
    wordAntonyms = []
    for sseq in entry["def"][0]["sseq"]:
      for sense in sseq: #iterate through the list of senses (meanings) for a given word. For each sense in the list of sense sequences, do x
        sense_data = sense[1] #skip to 1, as sense[0] is just "sense"
        if "dt" in sense_data: #if "defining text" is in the sense data of a particular, listed sense
          for dt_pair in sense_data["dt"]: #append the definition text to the list of defining text
            if dt_pair[0] == "text":
              wordDefinitions.append(dt_pair[1])
        if "syn_list" in sense_data: #if this is located in sense data, list all synonyms in the synonym list
          for syn_group in sense_data["syn_list"]:
            for syn_dict in syn_group:
              if "wd" in syn_dict:
                wordSynonyms.append(syn_dict["wd"])
        if "near_list" in sense_data: #if this is located in sense data, list all synonyms in the synonym list
          for near_group in sense_data["near_list"]:
            for near_dict in near_group:
              if "wd" in near_dict:
                wordNearSynonyms.append(near_dict["wd"])
        if "phrase_list" in sense_data:
          for syn_phrase_group in sense_data["phrase_list"]:
            for syn_phrase_dict in syn_phrase_group:
              if "wd" in syn_phrase_dict:
                wordPhraseSynonyms.append(syn_phrase_dict["wd"])
        if "ant_list" in sense_data:
          for ant_group in sense_data["ant_list"]:
            for ant_dict in ant_group:
              if "wd" in ant_dict:
                wordAntonyms.append(ant_dict["wd"])

      results.append({
        "word": wordToBeDefined,
        "type": wordType,
        "definitions": wordDefinitions,
        "synonyms": wordSynonyms,
        "phrase_synonyms": wordPhraseSynonyms,
        "near_synonyms": wordNearSynonyms,
        "antonyms": wordAntonyms
      })
      return results

running = True
while running:
  word = input("What word would you like to look up today?  ")
  if len(word) > 0: 
      defineThis = get_thesaurus(word)
      print(f"{defineThis}")
  else:
    print("Word was never inputted.")
  



#ctrl + / com,ment out multiple lines