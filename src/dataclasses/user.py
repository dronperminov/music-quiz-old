from dataclasses import dataclass

from src.dataclasses.settings import Settings


@dataclass
class User:
    username: str
    password_hash: str
    fullname: str
    settings: Settings
