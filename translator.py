import requests

from bs4 import BeautifulSoup

languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch',
             'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']

sentence_list = []
word_list = []

print("Hello, welcome to the translator. Translator supports:")
for i in range(len(languages)):
    print(f"{i + 1}.", languages[i])

print("Type the number of your language:")
src_language = int(input())

print("Type the number of language you want to translate to: ")
trg_language = int(input())

print("Type the word you want to translate:")
word_to_translate = input()

language_chain = f"{languages[src_language - 1]}-{languages[trg_language - 1]}".lower()

build_url = f"https://context.reverso.net/translation/{language_chain}/{word_to_translate}"
get_url = requests.get(build_url, headers={'User-Agent': 'Mozilla/5.0'})
get_html = BeautifulSoup(get_url.content, 'html.parser')

if get_url.status_code == 200:

    print(f"\n{languages[trg_language - 1]} Translations:")

    find_displayTerm = get_html.findAll("span", {"class": "display-term"})

    find_trgLtr = get_html.findAll("div", {"class": "trg ltr"})
    find_srcLtr = get_html.findAll("div", {"class": "src ltr"})

    for span in find_displayTerm:
        word_list.append(span.text)
    for i in range(5):
        print(word_list[i])

    print(f"\n{languages[trg_language - 1]} Examples:")
    for div in find_srcLtr:
        sentence_list.append(div.text.strip())
    for div in find_trgLtr:
        sentence_list.append(div.text.strip())

    for i in range(10):
        print(sentence_list[i])

else:
    print("Uh oh, that doesn't work.")
