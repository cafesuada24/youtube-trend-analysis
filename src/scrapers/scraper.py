from collections.abc import Iterable
from typing import Literal, Protocol


class Scraper(Protocol):
    def scrape_channels(
        self,
        channel_urls: Iterable[str],
        num_of_posts: int,
        start_date: str,
        end_date: str,
        order_by: str,
        country: str,
    ) -> None | dict: ...

    def get_progress(self, snapshot_id: str) -> None | dict: ...

    def get_output(
        self,
        snapshot_id: str,
        *,
        output_format: Literal['json', 'jsonl'],
    ) -> None | list[dict]: ...
