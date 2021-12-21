import logging
from fastapi import FastAPI
from models.website import Website

class App:
    def __init__(self) -> None:
        self.app = FastAPI()
        log = logging.getLogger("app")
        log.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        log.addHandler(ch)

        uktier2 = Website(name="UK Tier 2", url="https://www.uk-tier2.com/", body="UK Tier 2 is a UK-based provider of IT services and solutions.", protocol="https")

        @self.app.get("/")
        def root():
            return uktier2

    def getApi(self) -> FastAPI:
        return self.app