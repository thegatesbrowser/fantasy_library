from contextlib import asynccontextmanager
from typing import AsyncGenerator, Annotated


from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import uvicorn
from http import HTTPStatus
import httpx
from pydantic import Json
import asyncio

BOOK_URLS= {
    123: 'https://archive.org/download/historyofegyptch17324gut/17324.txt',
    456: 'https://archive.org/download/annakarenina01399gut/1399.txt'
}

'''
    Two kv stores - one for links, second for raw text

    - user picks a book by its id
    - if id is not in the raw text kvs
        - go to links kvs and download the book
        - save the text to raw text kvs
    - else parse params
    - then find the page from the raw text kvs
    - finally return it to the client
'''


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    print("Started the app")
    yield
    print("Stopped the app")


app = FastAPI(docs="hello this is fastapi app", lifespan=lifespan)


@app.get("/")
async def root() -> dict | str:
    return dict(name="app", hello="hi", user_agent="your mom")


@app.get('/books/{book_id}')
async def get_book(book_id: int) -> str:
    if (book_url := BOOK_URLS.get(book_id)) is None:
        return "error: no such book found" # TODO: discuss error signalling to the client 
    
        # TODO: check for bad page number
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(book_url)
            if resp.status_code == HTTPStatus.FOUND:
                # On 302, 'Location' header has the new link (what if there's another?)
                resp = await client.get(resp.headers["Location"])
            book = resp.text
    except Exception as e:
        return str(e)
        # return "error: couldn't download book for some reason"
            # TODO: handle errors properly
    
    return book[:1000]
        

if __name__ == "__main__":
    print(__name__)
    try:
        uvicorn.run(
            app="server:app", host="127.0.0.1", port=8000, reload=True, workers=1
        )
    except KeyboardInterrupt as e:
        print(e)
