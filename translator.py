import requests

from bs4 import BeautifulSoup

languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
             'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian',
             'Turkish']

print('Hello, welcome to the translator. The translator supports:')
for choice in range(len(languages)):
    print(f'{choice + 1}.', languages[choice])

print('Type the number of your language:')
src_language = int(input())

print('Type the number of language you want to translate to or 0 to translate to all languages:')
trg_language = int(input())

print('Type the word you would like to translate:')
word_to_translate = input()

def language_chain_factory(trg_language):
    language_chain = f'{languages[src_language - 1]}-{languages[trg_language]}'.lower()
    return language_chain

def api_factory(language_chain):
    build_url = f'https://context.reverso.net/translation/{language_chain}/{word_to_translate}'
    return build_url

def request_factory(build_url):
    get_url = requests.get(build_url, headers={'User-Agent': 'Mozilla/5.0'})
    return get_url

def html_factory(get_url):
    get_html = BeautifulSoup(get_url.content, 'html.parser')
    return get_html

def function_factory(trg_language):
    language_chain = language_chain_factory(trg_language)
    build_url = api_factory(language_chain)
    get_url = request_factory(build_url)
    get_html = html_factory(get_url)

    file_handler = open(f'{word_to_translate}.txt', mode='a', encoding='utf-8')

    def scrape_factory():

        word_list = []

        src_sentence_list = []
        trg_sentence_list = []

        find_display_term = get_html.findAll('span', {'class': 'display-term'})

        find_trg_ltr = get_html.findAll('div', {'class': 'trg ltr'})
        find_src_ltr = get_html.findAll('div', {'class': 'src ltr'})

        find_src_arabic = get_html.findAll('div', {'class': 'src rtl'})
        find_trg_arabic = get_html.findAll('div', {'class': 'trg rtl arabic'})

        find_src_hebrew = get_html.findAll('div', {'class': 'src rtl'})
        find_trg_hebrew = get_html.findAll('div', {'class': 'trg rtl'})

        find_arabic_span = get_html.find('span', {'lang': 'ar'})

        for find_arabic_span in find_src_arabic:
            src_sentence_list.append(find_arabic_span.text.strip())
        for find_arabic_span in find_trg_arabic:
            trg_sentence_list.append(find_arabic_span.text.strip())

        for span in find_display_term:
            word_list.append(span.text)

        for div in find_src_ltr:
            src_sentence_list.append(div.text.strip())
        for div in find_src_hebrew:
            src_sentence_list.append(div.text.strip())
        for div in find_trg_ltr:
            trg_sentence_list.append(div.text.strip())
        for div in find_trg_hebrew:
            trg_sentence_list.append(div.text.strip())

        file_handler.write(f'\n{languages[trg_language]} Translations:\n')
        file_handler.write(word_list[0] + '\n')

        file_handler.write(f'\n{languages[trg_language]} Example:\n')
        file_handler.write(src_sentence_list[0] + '\n')
        file_handler.write(trg_sentence_list[0] + '\n')

        file_handler.close()

        read_file = open(f'{word_to_translate}.txt', mode='r', encoding='utf-8')
        print(read_file.read())

        read_file.close()

    if get_url.status_code == 200:
        scrape_factory()
    else:
        print('Uh oh, that does not work.')

if trg_language == 0:
    for lang in languages:
        if lang != languages[src_language - 1]:
            function_factory(languages.index(lang))
else:
    function_factory(trg_language - 1)
