from flask import Flask, Request, Response, request, make_response, url_for, redirect
import requests
from bs4 import BeautifulSoup, Tag, NavigableString
import re
import sys

HACKER_NEWS_HOST = "https://news.ycombinator.com"

app = Flask(__name__)


@app.route('/cr_st/', methods=['GET'])
def static_route_handler() -> Response:
    """обработчик маршрута для проксирования статики"""
    url = request.args.get('url')
    requests_response = requests.get(url)

    response = make_response(requests_response.content)
    response.headers['content-type'] = requests_response.headers['content-type']

    return response


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path: str) -> str:
    """ маршруты для навигации по относительным ссылкам хоста Hacker News """

    url = HACKER_NEWS_HOST + request.full_path
    # Получить исходный код запрошенного URL
    html = get_html(url, request)
    # распарсить исходный код и превратить в объект BeautifulSoup
    soup = BeautifulSoup(html, features="html5lib")
    # Переписать ссылки HACKER_NEWS_HOST на прокси
    soup = fix_link_hrefs(soup)
    # Завернуть относительные ссылки img/script/css на наш спец.роут для статики
    soup = fix_src(soup)
    # Добавить словам из 6 букв постфикс tm
    soup = add_tm(soup)

    return str(soup)


def fix_link_hrefs(soup: BeautifulSoup) -> BeautifulSoup:
    """Заменить хост в ссылках с абсолютными путями на хост прокси"""

    # Найдём ссылки (html тег <a>)
    tag: Tag
    tags = soup.findAll(['a'])
    # Регулярка для определения абсолютного URL (вида //:host/path)
    url_pattern = re.compile(
        "(https?:)?(//)(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)")

    for tag in tags:
        href = str(tag.get('href'))
        # проверяем абсолютный ли адрес у ссылки
        matches = re.match(url_pattern, tag.get('href'))
        # если адрес вообще задан и он абсолютный, то меняем
        if href and matches and re.search(HACKER_NEWS_HOST, href):
            newurl = href.replace(matches.group(0), request.root_url)
            tag['href'] = newurl

    return soup


def get_html(url: str, request: Request) -> str:
    """Получить с HackerNews данные запрошенным методом"""

    if request.method == 'GET':
        resp = requests.get(url)
    elif request.method == 'POST':
        print("POST Received: " + str(request.form.to_dict()), file=sys.stdout)
        try:
            resp = requests.request(
                request.method, url, data=request.form.to_dict())
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}", file=sys.stderr)
            return redirect(request.root_url, code=302)

    return resp.text


def fix_src(soup: BeautifulSoup) -> BeautifulSoup:
    """ Добавляет префикс cr_st/?url=<hacker_news_host> на все относительные пути, 
        указанные в атрибутах src или href 
    """
    tags = soup.findAll(['img', 'script', 'link'])
    r = re.compile("(https?:)?(//)(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)")
    for tag in tags:
        if tag.get('src') and not re.match(r, tag.get('src')):
            tag['src'] = url_for('static_route_handler',
                                 url=HACKER_NEWS_HOST + '/' + tag['src'])
        elif tag.get('href') and not re.match(r, tag.get('href')):
            tag['href'] = url_for('static_route_handler',
                                  url=HACKER_NEWS_HOST + '/' + tag['href'])
    return soup


def patch_str(s: str) -> str:
    """Добавляет tm в строки длиной 6 символов"""

    needed_words = re.findall(r"\b[A-zА-я]{6}\b", s)
    for word in needed_words:
        s = s.replace(word, word+'™')
    return s


def add_tm(soup: BeautifulSoup) -> BeautifulSoup:
    """Находит на странице текст, который не является тегом
    Вызывает функцию добавления постфикса в виде tm
    Заменяет строку в коде странци пропатченной строкой
    """
    tag: Tag
    for tag in soup.find_all():
        if tag.string and not tag.find_all():
            tag.string = patch_str(tag.string)
        elif len(tag.contents) > 0 and not re.search(r"<|>", str(tag.contents[0])):
            # этот фрагмент обрабатывает случаи типа этого:
            #   <body>
            #    You have to be logged in to comment. < br/> < br/>
            #       <b > Login < /b > <br/> < br/>
            #   </body>
            # здесь тот текст, что сразу после открывающего body, не попадает в tag.string
            newval = patch_str(tag.contents[0])
            tag.contents[0] = NavigableString(newval)
    return soup


if __name__ == '__main__':
    app.run(debug=True, port=8000)
