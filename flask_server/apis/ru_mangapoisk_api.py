import re
import requests

from bs4 import BeautifulSoup
from abstract_api_classes import abstract_api


class mangapoisk_api(abstract_api):

    def __init__(self) -> None:
        super(mangapoisk_api, self).__init__()
        self.domen_name = 'https://mangapoisk.ru'
        
        self.regex_genres = re.compile(r'class="card-genres-item">([А-я0-9]+)<')
        self.regex_chapters = re.compile(r'<span>Глава: (\d+)<\/span>')
        self.regex_image_not_valid = re.compile(r'^data:image')
        self.regex_rating = re.compile(r'<span class="fa fa-star rating-star">\s+::before\s+\" (\d\.\d+)')

    # Private

    '''
    Returns dict of all manga available on given page
    '''
    def __get_books_from_page(self, page=None):
        if page == None:
            return {}

        html_data = BeautifulSoup(page, "html.parser")
        html_books = html_data.find_all("article") # Finds all the manga available on current page 
        catalog_dict = {}

        book_counter = 0
        for book in html_books:
            manga_title = book.find('a')['title']
            manga_url = book.find('a')['href']
            manga_url = self.domen_name + manga_url

            manga_cover = book.a.img['src']
            if self.regex_image_not_valid.match(manga_cover):
                manga_cover = book.a.img['data-src']

            manga_genres = self.regex_genres.findall(str(book))
            manga_chapters = self.regex_chapters.search(str(book)).group(1)

            manga_year = book.find('span', class_='js-card-year').text.strip()
            manga_year = manga_year.split(' ')[1]
            manga_description = book.find('p', class_='card-text').text.strip()

            manga_rating = book.find('span', class_='fa fa-star rating-star')
            if manga_rating:
                manga_rating.text.strip()
            else:
                manga_rating = None

            catalog_dict['manga_' + str(book_counter)] = {'title': manga_title, 'genres': manga_genres, 'chapters': manga_chapters, 
                                                        'year': manga_year, 'rating': manga_rating, 'description': manga_description, 
                                                        'url': manga_url, 'cover': manga_cover}
            book_counter += 1

        return catalog_dict

    def __get_html_code(self, url=None):
        if url == None:
            return url
        try:
            html_page = requests.get(url)
        except Exception as ex:
            print(ex)
        
        if html_page.status_code == 200:
            return html_page.text
        else:
            print("Something went wrong, we get response " + str(html_page.status_code))

        return None

    # Public

    '''
    Returns dict of manga available on catalog page
    By default returns first page of the catalog
    '''
    def get_catalog(self, page=1):
        catalog_dict = {}
        catalog_page = self.__get_html_code('https://mangapoisk.ru/manga?page=' + str(page))

        if catalog_page:
            return self.__get_books_from_page(catalog_page)
        
        return None

    '''
    Returns dict of manga satisfying the request title
    Returns empty dict if nothing found
    '''
    def search(self, title=None):
        if title == None:
            return None
        search_string = title.replace(' ', '+')
        search_request = self.domen_name + '/search?q=' + search_string
        return self.__get_books_from_page(self.__get_html_code(search_request))

fds = mangapoisk_api()
page = fds.search('Истории монстров')
print(page)