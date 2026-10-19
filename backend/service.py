from flask import jsonify
from models import PersonalText
from smart_search import all_public_texts, smart_search

def success_response(data=None, message=None, meta=None, code=200):
    response = {"status": "success"}

    if message:
        response["message"] = message

    if data is not None:
        response["data"] = data

    if meta:
        response["meta"] = meta

    return jsonify(response), code           


def error_response(message, errors=None, code=400):
    response = {
        "status": "success",
        "message": message
    }

    if errors:
        response["errors"] = errors

    return jsonify(response), code   

def custom_paginate(data: list, page: int = 1, per_page: int = 20):
    start = (page - 1) * per_page
    end = start + per_page if start + per_page < len(data) else len(data) - 1
    return data[start:end]

def process_public_texts_search(
        per_page:  int = 20, 
        page: int = 1,
        query: str = None, 
        from_word_count: int = None, 
        to_word_count: int = None 
        ):


    is_var_fwc = from_word_count is not None
    is_var_twc = to_word_count is not None

    if query is None and from_word_count is None and to_word_count is None:
        return all_public_texts.paginate(page, per_page)

    if is_var_fwc or is_var_twc:

        if query is None:
            def word_count_conditions() -> list:
                if not is_var_twc:
                    return  [PersonalText.word_count >= from_word_count]

                if not is_var_fwc:
                    return [PersonalText.word_count <= to_word_count]

                return [PersonalText.word_count >= from_word_count, PersonalText.word_count <= to_word_count]

            return all_public_texts.where(*word_count_conditions()).paginate(page, per_page)


        def is_valid_word_count(text: PersonalText) -> bool:

            if not is_var_twc:
                return  text.word_count >= from_word_count

            if not is_var_fwc:
                return text.word_count <= to_word_count

            return text.word_count >= from_word_count and text.word_count <= to_word_count

        word_count_filtred = list(filter(is_valid_word_count, all_public_texts))
        query_filtred = smart_search(query, word_count_filtred)
        return custom_paginate(query_filtred, page, per_page)
    else:
        query_filtred = smart_search(query, all_public_texts)
        return custom_paginate(query_filtred, page, per_page)

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