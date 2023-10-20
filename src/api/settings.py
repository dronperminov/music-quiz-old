from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src.api import templates
from src.database import database
from src.utils.auth import get_current_user

router = APIRouter()


@router.get("/settings")
def settings(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    template = templates.get_template("settings.html")
    content = template.render(user=user, page="settings")
    return HTMLResponse(content=content)


@router.post("/settings")
async def update_settings(request: Request, user: Optional[dict] = Depends(get_current_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    data = await request.json()

    user["fullname"] = data["fullname"]
    user["settings"]["theme"] = data.get("theme", user["settings"]["theme"])

    database.users.update_one({"username": user["username"]}, {"$set": user}, upsert=True)
    return JSONResponse({"status": "success"})
