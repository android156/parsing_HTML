from requests import get
import json
from os import listdir
from time import sleep
from bs4 import BeautifulSoup as bs
import re
from pymongo import MongoClient


def print_dictionary_values(dict):
    for key in dict:
        print(f'{key} - {dict[key]}')
    print('\n\n\n')

def print_list_values(list):
    for el in list:
        print(f'{el}')

def get_page(url, params, page=0):

    req = get(url, params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    return data


def get_soup(html):
    return bs(html, features="lxml")


def is_substring_in_strings_list(substring, list_of_strings):
    for string in list_of_strings:
        if substring in string:
            return True
    return False


client = MongoClient('localhost', 27017)
db = client['vacancy_db']
collection = db.vacancies


# Нашли путь, где вакансии расположены, поддерживается пагинациz, можно менять параметр page
page = 1
url_sj = 'https://www.superjob.ru/vacancy/search/'

params_sj = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'geo[t][0]': 4,  # Поиск ощуществляется по вакансиям города Москва
    'page': page,  # страница при пагинации SJ
    }

# В комментариях почему-то была ссылка на API с HH. С API доставать мы уже умеем.
url_hh = 'https://api.hh.ru/vacancies'
params_hh = {
        'text': 'NAME:Аналитик',  # Текст фильтра. В имени должно быть слово "Аналитик"
        'area': 1,  # Поиск ощуществляется по вакансиям города Москва
        'page': page,  # Индекс страницы поиска на HH
        'per_page': 20  # Кол-во вакансий на 1 странице
    }

req = get(url_sj, params_sj).text
soup = bs(req, features="lxml")

vacancy_div_cards = soup.find_all('div', attrs={'f-test-search-result-item'})
tags_a = soup.find_all(['a'])
tags_attrs = [tag.attrs for tag in tags_a]

print(f'Тэги, которые содержат в атрибуте "class" подстроку "f-test-link-":')
counter = 1
for tag in tags_a:
    if is_substring_in_strings_list('f-test-link-', tag.attrs['class']):
        print(f'{counter}. Тэг: "{tag.name}" Содержимое:\n{tag.contents}')
        counter += 1
        if tag.string:
            print(f'Текстовое поле: {tag.string}')
        print(f'Все его атрибуты:\n{tag.attrs}')

counter = 1
for tag in tags_a:
    if 'icMQ_' in tag.attrs['class'] and \
            is_substring_in_strings_list('f-test-link-', tag.attrs['class']) and \
            '/vakansii/' in tag.attrs['href'] and tag.string and tag.string != 'Каталог профессий':
        print(f'{counter}. {tag.string}')
        counter += 1



# # div_vacancy_cards = soup.find_all(re.compile("^f-test-link"))
# print(vacancy_links)
# for vacancy_link in vacancy_links:
#     # vacancy = vacancy_card.find('f-test-link')
#     print(vacancy_link)
#     # print(f'vacancy - {vacancy}')
#     # print(divs)

# print(divs.contents)
# jsObj = json.loads(get_page(url_hh, params_hh))
# print(jsObj)

# soup.find_all(lambda tag: len(tag.name) == 1 and not tag.attrs)
# soup.find_all(lambda tag: len(tag.attrs) == 2)
# f-test-link
