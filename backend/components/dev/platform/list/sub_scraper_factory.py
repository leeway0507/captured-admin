from typing import List, Any
from abc import ABC, abstractmethod
from bs4 import Tag
from components.dev.utils.browser_controller import PageController as P
from .sub_scraper import PwKreamListSubScraper, PlatformListSubScraper


class PlatformListSubScraperFactory:
    def kream(self) -> PlatformListSubScraper:
        ...

    def stockX(self) -> PlatformListSubScraper:
        ...


class PwPlatformListSubScraperFactory(PlatformListSubScraperFactory):
    def __init__(self, page: P, min_volume: int, min_wish: int):
        self.page = page
        self.min_volume = min_volume
        self.min_wish = min_wish

    def kream(self) -> "PlatformListSubScraper":
        return PwKreamListSubScraper(self.page, self.min_volume, self.min_wish)
