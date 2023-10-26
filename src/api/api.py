from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from src import constants
from src.api import templates
from src.database import database
from src.utils.auth import get_current_user
from src.utils.statistic import get_statistic

router = APIRouter()


@router.get("/")
def index(user: Optional[dict] = Depends(get_current_user)) -> HTMLResponse:
    template = templates.get_template("index.html")

    usernames = database.statistic.distinct("username")
    statistics = dict()

    for username in usernames:
        statistics[username] = get_statistic(username)
        statistics[username]["image"] = database.users.find_one({"username": username}, {"image_src": 1})["image_src"]

    usernames = sorted(usernames, key=lambda username: -statistics[username]["questions"])[:constants.TOP_COUNT]
    content = template.render(user=user, page="index", version=constants.VERSION, statistics=statistics, usernames=usernames)
    return HTMLResponse(content=content)


@router.get("/profile")
def profile(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    # day_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # day_end = day_start + datetime.timedelta(days=1, microseconds=-1)
    statistic = get_statistic(user["username"])

    template = templates.get_template("profile.html")
    content = template.render(user=user, page="profile", version=constants.VERSION, statistic=statistic)
    return HTMLResponse(content=content)
