from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from src.api import templates
from src.utils.auth import get_current_user

router = APIRouter()


@router.get("/")
def index(user: Optional[dict] = Depends(get_current_user)) -> HTMLResponse:
    template = templates.get_template("index.html")
    content = template.render(user=user, page="index")
    return HTMLResponse(content=content)
