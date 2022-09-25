from pickle import NONE
import requests

from enum import Enum

from abc import ABC
from abc import abstractmethod
from abc import abstractclassmethod


class abstract_api(ABC):

    def __init__(self)-> None:
        super(abstract_api, self).__init__()
        self.domen_name = None
        self.domen_mirrors = []

    # Internal

    @abstractmethod
    def _get_books_from_page(self, page=None):
        if page == None:
            return {}

    @abstractmethod
    def _get_html_code(self, url=None):
        if url == None:
            return url

    # Public

    '''
    Returns dict of manga available on catalog page
    By default returns first page of the catalog
    '''
    @abstractmethod
    def get_catalog(self, page=0):
        pass
    
    @abstractmethod
    def get_manga(self, url:str=None):
        if url == None:
            return None

    '''
    Returns dict of manga satisfying the request title
    Returns empty dict if nothing found
    '''
    @abstractmethod
    def search(self, title=None):
        if title == None:
            return None


class release_status(Enum):
    ONGOING = 0
    COMPLETE = 1
    NONE = 2


class meta_manga():

    def __init__(self, release_year=None, page_count=None, chapter_count=None, rating=None,
                        genres=[], source_url=None, title=None, description=None, cover_img=None, status=None)-> None:
        self.release_year = release_year
        self.page_count = page_count
        self.chapter_count = chapter_count
        self.rating = rating
        self.genres = genres
        self.source_url = source_url  # URL link to manga page on site
        self.title = title
        self.description = description
        self.cover_img = cover_img   # URL link to manga cover
        self.status = status

    def __str__(self) -> str:
        return "{}, {}, {},".format(self.title, self.source_url, self.cover_img)

    # Public

    def get_json(self):
        return {'title': self.title, 'pages_count': self.page_count, 'chapter_count': self.chapter_count, 'genres': self.genres,
                'release_year': self.release_year, 'rating': self.rating, 'description': self.description, 'status': self.status,
                'source_url': self.source_url, 'cover_img': self.cover_img}
