import requests
from urllib.parse import quote


def get_larger_dictionary(word):
    encoded_word = quote(word)
    found_word = word.upper()
    url = f"https://freedictionaryapi.com/api/v1/entries/all/{encoded_word}"
    
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

    x=0
    for entry in data["entries"]:
        print(f"\n=========\n{x+1}. {entry["language"]["name"]}")
        print(f"({entry["partOfSpeech"]})")
        
        print(f"=========\n\nForms of {found_word} include:")
        numbered_list_of_forms = 1
        for forms in entry["forms"]:     
           print(f"\n{numbered_list_of_forms}.")
           print(forms["word"])
           print(forms["tags"])
           numbered_list_of_forms+=1

        definitions = entry.get("definition", [])
        tags = entry.get("tags", [])
        examples = entry.get("examples", [])
        
        for senses in (entry["senses"]):
           if definitions:
            print(f"\n\n\nDEFINITION - {senses["definition"]}")
           if tags: 
            print(f"\n{senses["tags"]}")
           if examples:
            print(f"\n{senses["examples"]}")

        synonyms = entry.get("synonyms", [])
        antonyms = entry.get("antonyms", [])
           
        if synonyms:
            print(f"\n=========\nSYNONYMS\n\n{entry["synonyms"]}\n")
        if antonyms:
            print(f"\n\nANTONYMS\n\n{entry["antonyms"]}\n\n")
        x+=1
    return
    
running = True
while running:
    word = input("\nWhat word would you like to look up today? ").strip()
    if word:
        results = get_larger_dictionary(word)                 
    else:
        print("Word was never inputted.")
