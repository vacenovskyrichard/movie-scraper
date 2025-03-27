from typing import Final

USER_AGENTS: Final[list] = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59"
]

CSFD_BASE_URL: Final[str] = "https://www.csfd.cz/"

TOP_300_FILMS_URLS: Final[list] = ["https://www.csfd.cz/zebricky/filmy/nejlepsi",
                                   "https://www.csfd.cz/zebricky/filmy/nejlepsi/?from=100",
                                   "https://www.csfd.cz/zebricky/filmy/nejlepsi/?from=200"]
