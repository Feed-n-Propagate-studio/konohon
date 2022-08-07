from enum import Enum
from abc import abstractmethod
from abc import abstractclassmethod


class abstract_api():

    def __init__(self)-> None:
        super(abstract_api, self).__init__()
        self.domen_name = None
        self.domen_mirrors = []

    @abstractmethod
    def get_catalog(self):
        pass

    @abstractmethod
    def search(self, title=None, genre=None, status=None, year=None, tags=[]):
        pass


class release_status(Enum):
    ONGOING = 0
    COMPLETE = 1


class abstract_manga():

    def __init__(self)-> None:
        self.release_year = None
        self.page_count = None
        self.chapter_count = None
        self.rating = None
        self.genres = []
        self.source_url = None  # URL link to manga page on site
        self.title = None
        self.description = None
        self.cover_img = None   # URL link to manga cover
        self.status = release_status.COMPLETE

    def get_json(self):
        return {'title': self.title, 'pages_count': self.page_count, 'chapter_count': self.chapter_count, 'genres': self.genres,
                'release_year': self.release_year, 'rating': self.rating, 'description': self.description, 'status': self.status,
                'source_url': self.source_url, 'cover_img': self.cover_img}
