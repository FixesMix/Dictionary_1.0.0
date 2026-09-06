import requests
from secrets import API_KEY
from urllib.parse import quote

#Typing in a word will show the complete definition along with synonyms and antonyms. You can select synonyms/antonyms in order to view definition of those along wth more
#synonyms/antonyms.

def get_thesaurus(word):
  encoded_word = quote(word)
  url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{encoded_word}?key={API_KEY}"
  print(url)
  
  try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
  except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None
  except requests.exceptions.JSONDecodeError:
        print("Invalid server data.")
        return None

  if not data:
        print(f"No results found for '{word}'.")
        return None

  if isinstance(data[0], str):
        print(f"'{word}' wasn't found.")
        return None

  results = []

  for entry in data:
        if not isinstance(entry, dict):
            continue

        wordToBeDefined = entry["hwi"]["hw"]
        wordType = entry["fl"]

        wordDefinitions = []
        wordSynonyms = []
        wordNearSynonyms = []
        wordPhraseSynonyms = []
        wordAntonyms = []

        for sseq in entry["def"][0]["sseq"]:
            for sense in sseq:
                sense_data = sense[1]
                if "dt" in sense_data:
                    for dt_pair in sense_data["dt"]:
                        if dt_pair[0] == "text":
                            wordDefinitions.append(dt_pair[1])
                if "syn_list" in sense_data:
                    for syn_group in sense_data["syn_list"]:
                        for syn_dict in syn_group:
                            if "wd" in syn_dict:
                                wordSynonyms.append(syn_dict["wd"])
                if "near_list" in sense_data:
                    for near_group in sense_data["near_list"]:
                        for near_dict in near_group:
                            if "wd" in near_dict:
                                wordNearSynonyms.append(near_dict["wd"])
                if "phrase_list" in sense_data:
                    for phrase_group in sense_data["phrase_list"]:
                        for phrase_dict in phrase_group:
                            if "wd" in phrase_dict:
                                wordPhraseSynonyms.append(phrase_dict["wd"])
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


def display_word(word, word_type, definitions, synonyms, phrase_synonyms, near_synonyms, antonyms):
    print("\n" + "=" * 50)
    print(f"{word.upper()} ({word_type})")
    print("=" * 50)
    print("\nWord Definition:")
    for i, d in enumerate(definitions, 1):
        print(f"  {i}. {d}")
    if synonyms:
        print("\nSynonyms:")
        print("  " + ", ".join(synonyms))
    if phrase_synonyms:
        print("\nSynonym Phrases:")
        print("  " + ", ".join(phrase_synonyms))
    if near_synonyms:
        print("\nNear synonyms:")
        print("  " + ", ".join(near_synonyms))
    if antonyms:
        print("\nAntonyms:")
        print("  " + ", ".join(antonyms))


running = True
while running:
    word = input("\nWhat word would you like to look up today? ").strip()
    if word:
        results = get_thesaurus(word)     
        if results is not None:
            for entry in results:               # loop through every part of speech
                display_word(entry["word"], entry["type"], entry["definitions"],
                             entry["synonyms"], entry["phrase_synonyms"],
                             entry["near_synonyms"], entry["antonyms"])
        else:
            print("Something went wrong looking that word up.")
    else:
        print("Word was never inputted.")



#ctrl + / com,ment out multiple lines