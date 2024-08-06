from fastapi.responses import Response, JSONResponse
from typing import TypeAlias
from http import HTTPStatus
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class BBCodeResponse(JSONResponse):
    def __init__(
        self,
        bbcode: str = "",
        images: list[dict[str, str]] = [],
        status: HTTPStatus = HTTPStatus.OK,
    ):
        super().__init__(
            status_code=status,
            content=dict(
                status=status,
                bbcode=bbcode,
                images=images
            )
        )


class ErrorResponse(JSONResponse):
    def __init__(
        self,
        status: HTTPStatus = HTTPStatus.NOT_FOUND,
        error: str = "",
        comment: str = "",
    ):
        super().__init__(
            status_code=status,
            content=dict(
                status=status,
                error_msg=error,
                comment=comment
            )
        ) # content value should be json-serializable

        # BBCodeResponse(status_code=400) should be valid


MyResponse: TypeAlias = ErrorResponse | BBCodeResponse
