from config import PAGE_SIZE
from typing import Generator


class Book:

    def __init__(self, text: str):
        self.text = text
        self.len = len(text)
        self.pages = self.len // PAGE_SIZE
    
    def __repr__(self) -> str:
        return f"<Book> {{chars: {self.len}, pages: {self.pages}}}"

    def get_page(self, page_number: int) -> str | None:
        assert page_number <= self.pages
        page_index = page_number - 1
        start = PAGE_SIZE * page_index
        if page_number == self.pages:
            return self.text[start:]
        return self.text[start: start + PAGE_SIZE]
             # TODO: think about prettier line breaks (spaces, commas, hyphens etc...)

    def get_text(self) -> str:
        return self.text

    def list_book(self) -> Generator[str, None, None]:
        i = 0
        while (page := self.get_page(i)):
            yield page
            i += 1