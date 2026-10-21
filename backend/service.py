from models import PublicText
from action_db import get_all_public_texts
from smart_search import smart_search
from utils import custom_paginate
from math import ceil

def list_of_public_text_to_dict(data: list[PublicText]) -> list[dict]:
    return [
        {
        "id": text.id,
        "title": text.title,
        "text": text.text,
        "category": text.category,
        "tags": text.tags,
        "word_count": text.word_count,
        } for text in data]


class ArgsValueError(Exception):
    pass
    
class PublicTextArgs():

    MAX_PER_PAGE = 90
    MIN_WORD_COUNT = 15
    MAX_WORD_COUNT = 280 

    def __init__(self, 
                 per_page:  int = 20, 
                 page: int = 1, 
                 query: str = None, 
                 from_word_count: int = None, 
                 to_word_count: int = None ):


        self.per_page = per_page # int, default 20
        self.page = page # int, default 1
        self.query = query # str | None, deflaut None
        self.from_word_count = from_word_count # int | None, from_word_count < to_word_count and from_word_count >= MIN_WORD_COUNT, default None
        self.to_word_count = to_word_count # int | None, to_word_count > from_word_count and to_word_count <= MAX_WORD_COUNT, default None


        if (self._from_word_count is not None
            and self._to_word_count is not None
            and self._from_word_count >= self._to_word_count):

            raise ArgsValueError("from_word_count must be less then to_word_count")

    @property
    def per_page(self):
        return self._per_page

    @per_page.setter
    def per_page(self, value: str | int):

        value = self.transform_into_a_number(value)
        
        if not 1 <= value <= self.MAX_PER_PAGE:
            raise ArgsValueError("Too many records for one request")

        self._per_page = value  


    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value: str | int):

        value = self.transform_into_a_number(value)

        if value < 1:
            raise ArgsValueError("Page cannot be less then one")

        self._page = value


    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value: str | None):

        if value is None:
            self._query = None
            return

        if not isinstance(value, str):
            raise ArgsValueError("Query must be a string")

        self._query = value.strip() or None


    @property
    def from_word_count(self):
        return self._from_word_count

    @from_word_count.setter
    def from_word_count(self, value: str | int | None):

        if value is None:
            self._from_word_count = None
            return

        value = self.transform_into_a_number(value)

        if value < self.MIN_WORD_COUNT or value > self.MAX_WORD_COUNT:
            raise ArgsValueError("The value out of range")

        self._from_word_count = value


    @property
    def to_word_count(self):
        return self._to_word_count

    @to_word_count.setter
    def to_word_count(self, value: str | int | None):

        if value is None:
            self._to_word_count = None
            return

        value = self.transform_into_a_number(value)

        if value < self.MIN_WORD_COUNT or value > self.MAX_WORD_COUNT:
            raise ArgsValueError("The value out of range")

        self._to_word_count = value    


    @staticmethod
    def transform_into_a_number(value: str | int) -> int:

        if isinstance(value, bool):
            raise ArgsValueError("The value must be an integer")

        if isinstance(value, int):
            return value

        if not isinstance(value, str):
            raise ArgsValueError("The value must be a string or integer")

        value = value.strip()

        if not value.isdecimal():
            raise ArgsValueError("The value must be a positive integer")

        return int(value)


class PublicTextService():
    ALL_TEXTS = get_all_public_texts() # ModelSelect

    def __init__(self, args: PublicTextArgs):
        self.args = args

        self.is_var_fwc = self.args.from_word_count is not None
        self.is_var_twc = self.args.to_word_count is not None
        self.is_var_query = self.args.query is not None

    
    def fetch_texts(self):

        if (not self.is_var_query
            and not self.is_var_fwc
            and not self.is_var_twc):

            total_pages = self.total_pages(self.ALL_TEXTS.count())
            return list(self.ALL_TEXTS.paginate(self.args.page, self.args.per_page)), total_pages

        if self.is_var_fwc or self.is_var_twc:

            if not self.is_var_query:

                conditions = self.word_count_conditions()
                result = self.ALL_TEXTS.where(*conditions)

                total_pages = self.total_pages(result.count())
                return result.paginate(self.args.page, self.args.per_page), total_pages

            
            word_count_filtred = list(filter(self.is_valid_word_count, self.ALL_TEXTS))
            query_filtred = smart_search(self.args.query, word_count_filtred)

            total_pages = self.total_pages(len(query_filtred))
            return custom_paginate(query_filtred, self.args.page, self.args.per_page), total_pages
        else:
            query_filtred = smart_search(self.args.query, self.ALL_TEXTS)
            total_pages = self.total_pages(len(query_filtred))

            return custom_paginate(query_filtred, self.args.page, self.args.per_page), total_pages

    def word_count_conditions(self) -> list[bool]:

        conditions = []

        if self.is_var_fwc:
            conditions.append(PublicText.word_count >= self.args.from_word_count)

        if self.is_var_twc:
            conditions.append(PublicText.word_count <= self.args.to_word_count)

        return conditions                        


    def is_valid_word_count(self, text: PublicText) -> bool:

        if self.is_var_fwc and text.word_count < self.args.from_word_count:
            return False

        if self.is_var_twc and text.word_count > self.args.to_word_count:
            return False

        return True

    def total_pages(self, total: int) -> int:
        return ceil(total / self.args.per_page)




