import contextlib
import json
from typing import Any

from fastapi import Query
from fastapi_pagination.default import Params
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.settings import settings


class PaginationParams(Params):
    """Pagination params schema class.

    Args:
        Params (_type_): _description_
    """

    size: int | None = Query(None, ge=0, le=500, description="Page size")


class EnvelopeResponseBody(BaseModel):
    """Envelope response body schema class.

    Args:
        BaseModel (_type_): _description_
    """

    links: Any | None = None
    count: Any | None = None
    results: Any | None = None


class ListEnvelopeResponseBody(EnvelopeResponseBody):
    """List envelope response body schema class.

    Args:
        EnvelopeResponseBody (_type_): _description_
    """

    results: list | None = None


class EnvelopeResponse(BaseModel):
    """Envelope response schema class.

    Args:
        BaseModel (_type_): _description_
    """

    errors: Any | None = None
    body: EnvelopeResponseBody | ListEnvelopeResponseBody | dict | None = None
    status_code: Any | None = None


def create_envelope_response(data, links=None, count=None):
    """Create envelope response data class.

    Args:
        data (_type_): _description_
        links (_type_, optional): _description_. Defaults to None.
        count (_type_, optional): _description_. Defaults to None.

    Returns
    -------
        _type_: _description_
    """
    body = EnvelopeResponseBody(links=links, count=count, results=data).model_dump()
    return EnvelopeResponse(errors=None, body=body)


def default_pagination_params(
    page: int = Query(1, ge=1, alias="page", description="Page number"),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=0, le=500, alias="page_size", description="Page size"),
) -> PaginationParams:
    """Add default pagination in the response class.

    Args:
        page (int, optional): _description_. Defaults to Query(1, ge=1, alias="page", description="Page number").
        page_size (int, optional): _description_. Defaults to Query(settings.DEFAULT_PAGE_SIZE, ge=0, le=500,
        alias="page_size", description="Page size").

    Returns
    -------
        PaginationParams: _description_
    """
    return PaginationParams(page=page, size=page_size)


def envelope_response(
    data: dict | None = None,
    links=None,
    count: int | None = None,
    errors: dict | None = None,
    status: int | None = None,
) -> JSONResponse:
    """Generate standart output json.

    Args:
        data (dict, optional): Output data.
        links (<<>>, optional): Link to paginate.
        count (int, optional): Count of elements.
        errors (dict, optional): Output errors.
        status (int, optional): Response status.

    Returns
    -------
        JSONResponse: Structured output
    """
    response_content = None
    if errors:
        response_content = {"errors": errors, "body": response_content}
    else:
        response_content = {"links": links, "count": count, "results": data}

    return JSONResponse(content=response_content, status_code=status)


def send_error_response(error: str):
    """Return error response format.

    Args:
        error (str): _description_

    Returns
    -------
        _type_: _description_
    """
    with contextlib.suppress(TypeError):
        error = json.loads(error)

    return envelope_response(
        errors={
            "error": "Error al obtener los datos",
            "error_detail": f"{error}",
        },
        status=404,
    )


def envelope_error_response(
    errors: dict | None = None,
    status: int | None = None,
    *args,  # noqa: ARG001
    **kwargs,  # noqa: ARG001
) -> JSONResponse:
    """Generate standart output json.

    Args:
        errors (dict, optional): Output errors.
        status (int, optional): Response status.

    Returns
    -------
        JSONResponse: Structured output
    """
    response_content = {"errors": errors, "body": None, "status_code": status}
    return JSONResponse(content=response_content, status_code=status)
