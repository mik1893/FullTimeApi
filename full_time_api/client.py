"""HTTP client for Full-Time URLs."""

from urllib.parse import urlencode

import requests


class FullTimeClient:
    """Fetches HTML from Full-Time URLs."""

    def get(self, url: str, params: dict | None = None) -> str:
        """GET a URL and return the response body as text."""
        url = self._build_url(url, params or {})
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch data from {url}: {e}") from e

    def _build_url(self, url: str, params: dict) -> str:
        if params:
            url = f"{url}?{urlencode(params)}"
        return url
