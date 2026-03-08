"""HTML parsing and XPath helpers."""

from lxml.html import fromstring


def create_dom_xpath(html_body: str):
    """Parse HTML string and return the document; use .xpath(expr) for queries."""
    return fromstring(html_body)
