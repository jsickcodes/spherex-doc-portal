"""Handlers for the portal's webpages."""

from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from safir.dependencies.logger import logger_dependency
from starlette.requests import Request
from starlette.templating import Jinja2Templates, _TemplateResponse
from structlog.stdlib import BoundLogger

from spherexportal.repository import DocumentRepository, repository_dependency

__all__ = ["router"]

router = APIRouter()
"""FastAPI router for webpages."""


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@router.get("/")
async def get_homepage(
    request: Request,
    logger: BoundLogger = Depends(logger_dependency),
    repo: DocumentRepository = Depends(repository_dependency),
) -> _TemplateResponse:
    context = {"request": request, "ssdc_ms": repo.get_ms_by_handle()}
    return templates.TemplateResponse("index.html", context)


@router.get("/__healthz")
async def get_healthz(
    repo: DocumentRepository = Depends(repository_dependency),
) -> PlainTextResponse:
    return PlainTextResponse("OK")
