from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Annotated, NoReturn, TypeAlias

from fastapi import FastAPI, Request, Path, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.encoders import jsonable_encoder
import uvicorn
from http import HTTPStatus
import httpx

from responses import BBCodeResponse, ErrorResponse


BOOK_URLS = {
    123: "https://www.gutenberg.org/ebooks/17321.txt.utf-8",
    456: "https://archive.org/download/annakarenina01399gut/1399.txt", # gets loaded for too long fmor archive
    789: "https://www.gutenberg.org/ebooks/1399.txt.utf-8"
}



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    print("Started the app")
    yield
    print("Stopped the app")


app = FastAPI(docs="hello this is fastapi app", lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.args[0][0]
    error_msg = f"{error['type']}: param '{error['input']}' is invalid"
    comment = f"{error['msg']}"
    return ErrorResponse(HTTPStatus.BAD_REQUEST, error_msg, comment)



@app.exception_handler(HTTPStatus.NOT_FOUND)
async def not_found(*args):
    return ErrorResponse(
        HTTPStatus.NOT_FOUND, "not found", "this resource doesn't exist"
    )


@app.get(
    "/test/{id}", response_model=None
)   # response_model is a factory which is called on a return value
    # on by deafult, should be off because 'Response's are not valid Pydantic types (=not children of BaseModel)
async def test(id: int) -> NoReturn | JSONResponse:
    raise ZeroDivisionError


@app.get("/")
async def root() -> dict | str:
    return dict(name="app", hello="hi", user_agent="your mom")


@app.get("/books/{book_id}", response_model=None)
async def get_book(book_id: int) -> JSONResponse:
    if (book_url := BOOK_URLS.get(book_id)) is None:
        return ErrorResponse(
            HTTPStatus.NOT_FOUND,
            "book not found",
            f"book id '{book_id}' is non-existent",
        )

        # TODO: check for bad page number
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(book_url)
            while resp.status_code == HTTPStatus.FOUND:
                resp = await client.get(resp.headers["Location"])
                # On 302, 'Location' header has the new link
            book = resp.text
    except Exception as e:
        return ErrorResponse(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            str(e),
            "something happened during book download",
        )
    return BBCodeResponse(bbcode=book[:1000])


if __name__ == "__main__":
    print(__name__)
    try:
        uvicorn.run(
            app="server:app", host="127.0.0.1", port=8000, reload=True, workers=1
        )
    except KeyboardInterrupt as e:
        print(e)
