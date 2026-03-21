from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any, Dict


class BaseScraper(ABC):
    """
    Base class for all tender scrapers.

    Each scraper should implement `fetch_tenders` and return an iterable of
    normalized tender dictionaries.
    """

    source_slug: str

    @abstractmethod
    def fetch_tenders(self) -> Iterable[Dict[str, Any]]:
        """
        Yield dictionaries with keys:
        external_id, title, description, department, category,
        province, published_date, closing_date, url, raw_data.
        """
        raise NotImplementedError

