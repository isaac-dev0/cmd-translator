import requests
import sys

from bs4 import BeautifulSoup

languages = [ "arabic", "german", "english", "spanish", "french",
              "hebrew", "japanese", "dutch", "polish", "portuguese",
              "romanian", "russian", "turkish" ]

word = 'DEFAULT'

args = sys.argv

def contains_args():
    if len(sys.argv) > 1:
        return True
    else:
        return False

def welcome():
    # Checking if the user is passing in args or not.
    if contains_args() == True:
        # Taking args for source_language, target_language and word - converting them to lowercase.4 
        source_language = args[1].lower()
        target_language = args[2].lower()
        word = args[3].lower()
        file = open(f'{word}.txt', mode='w', encoding='utf-8')
        # Passing in target_language to all() and checking if True or False.
        if all(target_language) == True:
            # Getting the list index of the user's input for source_language.
            source_language_index = languages.index(source_language)
            # Getting the index of each language in the languages list
            for language in languages:
                target_language_index = languages.index(language)
                query(source_language_index, target_language_index, word, file)
        # If the user doesn't enter 'all' as target_language, run this block of code.
        else:
            source_language_index = languages.index(source_language)
            target_language_index = languages.index(target_language)
            query(source_language_index, target_language_index, word, file)
    else:
        print("Hello, welcome to the translator. The translator supports:")
        
        for language in range(len(languages)):
            print(languages[language])

        print("Enter the language you would like to translate from.")
        source_language = str(input())

        print("Enter the language you would like to translate to.")
        target_language = str(input())

        print("Enter the word you would like to translate.")
        word = str(input())

        file = open(f'{word}.txt', mode='w', encoding='utf-8')
        query(source_language, target_language, word, file)

    file.close()
    
    file = open(f'{word}.txt', mode='r', encoding='utf-8')
    print(file.read())
    file.close()

def all(target_language):
    if target_language == 'all':
        return True
    else: 
        return False

def query(source_language_index, target_language_index, word, file):
    url = f"https://context.reverso.net/translation/{languages[source_language_index]}-{languages[target_language_index]}/{word}"
    header = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    parser = BeautifulSoup(header.content, 'html.parser')

    translated_words = parser.findAll('span', {'class': 'display-term'})
    source_sentences = parser.findAll('div', {'class': 'src ltr'})

    if languages[target_language_index] == "arabic":
        target_sentences = parser.findAll('div', {'class': 'trg rtl arabic'})
        
    elif languages[target_language_index] == "hebrew":
        target_sentences = parser.findAll('div', {'class': 'trg rtl'})

    else:
        target_sentences = parser.findAll('div', {'class': 'trg ltr'})

    file.write(f'{languages[target_language_index].capitalize()} Translations:\n')
    for word in translated_words[:5]:
        file.write(f'{word.text}\n')

    file.write(f'\n{languages[target_language_index].capitalize()} Examples:\n')
    for (a, b) in zip(source_sentences[:5], target_sentences[:5]):
        file.write(f'{a.text.strip()}\n{b.text.strip()}\n\n')


welcome()
