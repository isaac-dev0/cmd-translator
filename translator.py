import requests

from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0'}
language_chain = ""

language = ""

sentence_list = []
word_list = []

print("Type 'en' if you want to translate from French to English, or 'fr' if you want to translate from English into French.")
language_input = input()
if language_input == "fr":
    language_chain = "english-french"
    language = "French"
elif language_input == "en":
    language_chain = "french-english"
    language = "English"
else:
    print("Invalid language. Please try a different one! :D")

print("Type the word you would like to translate.")
word_to_translate = input()

print("You have chosen ", language_input, " as a language to translate", word_to_translate, ".")

build_url = f"https://context.reverso.net/translation/{language_chain}/{word_to_translate}"
get_url = requests.get(build_url, headers=headers)
get_html = BeautifulSoup(get_url.content, 'html.parser')

if get_url.status_code == 200:
    print(get_url.status_code, "OK")

    print(f"\n{language} Translations:")

    find_displayTerm = get_html.findAll("span", {"class": "display-term"})

    find_trgLtr = get_html.findAll("div", {"class": "trg ltr"})
    find_srcLtr = get_html.findAll("div", {"class": "src ltr"})

    for span in find_displayTerm:
        word_list.append(span.text)
    for i in range(5):
        print(word_list[i])

    print(f"\n{language} Examples:")
    for div in find_srcLtr:
        sentence_list.append(div.text.strip())
    for div in find_trgLtr:
        sentence_list.append(div.text.strip())

    for i in range(10):
        print(sentence_list[i])

else:
    print("Uh oh, that doesn't work.")
