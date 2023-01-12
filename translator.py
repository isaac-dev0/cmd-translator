import requests
import sys

from bs4 import BeautifulSoup

# List of languages that the translator can translate to and from.
languages = [ "arabic", "german", "english", "spanish", "french",
              "hebrew", "japanese", "dutch", "polish", "portuguese",
              "romanian", "russian", "turkish", "all" ]

# Default word to translate
word = 'DEFAULT'

args = sys.argv

# Function to check if user passed any command line arguments
def contains_args():
    if len(sys.argv) > 1:
        return True
    else:
        return False

def welcome():
    try:
        # Checking if the user is passing in args or not.
        if contains_args() == True:
            # Taking args for source_language, target_language and word - converting them to lowercase.4
            source_language = args[1].lower()
            target_language = args[2].lower()
            word = args[3].lower()
            #checking if the inputed languages are supported
            if source_language not in languages:
                raise ValueError(f"Sorry, the program doesn't support {source_language}")
            if target_language not in languages:
                raise ValueError(f"Sorry, the program doesn't support {target_language}")
            if source_language == target_language:
                raise ValueError(f"Source and target languages must be different.")
            # Opening the file stream.
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
            if source_language not in languages:
                raise ValueError(f"Sorry, the program doesn't support {source_language}")
            source_language_index = languages.index(source_language)

            print("Enter the language you would like to translate to.")
            target_language = str(input())
            if target_language not in languages:
                raise ValueError(f"Sorry, the program doesn't support {target_language}")
            target_language_index = languages.index(target_language)

            if source_language == target_language:
                raise ValueError(f"Source and target languages must be different.")

            print("Enter the word you would like to translate.")
            word = str(input())

            file = open(f'{word}.txt', mode='w', encoding='utf-8')
            query(source_language_index, target_language_index, word, file)

        # Closing the file and opening it to read the contents
        file.close()

        file = open(f'{word}.txt', mode='r', encoding='utf-8')
        print(file.read())
        file.close()
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to check if the target language is "all"
def all(target_language):
    if target_language == 'all':
        return True
    else:
        return False

# Function that sends a request to the website and scrapes for translation data
def query(source_language_index, target_language_index, word, file):
    url = f"https://context.reverso.net/translation/{languages[source_language_index]}-{languages[target_language_index]}/{word}"
    try:
        try:
            header = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            parser = BeautifulSoup(header.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print("Something went wrong with your internet connection")

        # Scraping translated words
        translated_words = parser.findAll('span', {'class': 'display-term'})

        if not parser.findAll('span', {'class': 'display-term'}):
            print(f"Sorry, unable to find {word}")
            return

        # Scraping source sentences
        source_sentences = parser.findAll('div', {'class': 'src ltr'})

        # Scraping target sentences
        if languages[target_language_index] == "arabic":
            target_sentences = parser.findAll('div', {'class': 'trg rtl arabic'})

        elif languages[target_language_index] == "hebrew":
            target_sentences = parser.findAll('div', {'class': 'trg rtl'})

        else:
            target_sentences = parser.findAll('div', {'class': 'trg ltr'})

        # Writing data to file
        file.write(f'{languages[target_language_index].capitalize()} Translations:\n')
        for word in translated_words[:5]:
            file.write(f'{word.text}\n')

        # Writing the source and target sentences
        file.write(f'\n{languages[target_language_index].capitalize()} Examples:\n')
        for (a, b) in zip(source_sentences[:5], target_sentences[:5]):
            file.write(f'{a.text.strip()}\n{b.text.strip()}\n\n')
    except Exception as e:
        print(f"An error occurred while querying: {e}")

# Calling the main function
welcome()
