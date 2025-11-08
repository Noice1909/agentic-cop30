# tools/parse.py
from bs4 import BeautifulSoup
import re

def to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    # drop nav/footers/scripts
    for tag in soup(["script","style","noscript","header","footer","aside","nav"]):
        tag.decompose()
    # get title if needed elsewhere
    # normalize
    text = " ".join(t.strip() for t in soup.get_text(separator=" ").split())
    # collapse multiple spaces
    text = re.sub(r"\s{2,}", " ", text)
    return text
