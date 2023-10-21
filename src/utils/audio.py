import re
import traceback

import requests
from bs4 import BeautifulSoup


def parse_audio_html(html: str) -> dict:
    if not html.strip():
        return {"status": "error", "message": "html код пуст"}

    if html.startswith("https://"):
        response = requests.get(html)

        if response.status_code != 200:
            return {"status": "error", "message": "не удалось получить исходный код страницы"}

        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        soup = soup.findAll("ul", class_="mainSongs")[0]
    else:
        soup = BeautifulSoup(html, "html.parser")

    try:
        audios = []

        for li in soup.findAll("li", class_="item"):
            link = li.findAll("li", class_="play")[0]["data-url"]
            description = li.findAll("div", class_="desc")[0]
            artist = re.sub(r"\s+", " ", description.findAll("span", class_="artist")[0].text).strip()
            track = re.sub(r"\s+", " ", description.findAll("span", class_="track")[0].text).strip()
            audios.append({"link": link, "artist": artist, "track": track})

        if not audios:
            return {"status": "error", "message": "не удалось распарсить ни одного аудио"}

        return {"status": "success", "audios": audios}
    except Exception:
        stacktrace = traceback.format_exc().replace("\n", "<br>")
        return {"status": "error", "message": f"не удалось распарсить html код<br>Стек вызовов: {stacktrace}"}
