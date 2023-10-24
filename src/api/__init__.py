import os
from typing import Optional

from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

templates = Environment(loader=FileSystemLoader("web/templates"), cache_size=0)

with open(os.path.join(os.path.dirname(__file__), "..", "..", "tokens.txt"), "r") as f:
    tokens = f.read().splitlines()


def make_error(message: str, user: Optional[dict]) -> HTMLResponse:
    template = templates.get_template("error.html")
    content = template.render(user=user, page="error", message=message)
    return HTMLResponse(content=content)
