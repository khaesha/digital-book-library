
# Import httpx for making async HTTP requests
import httpx
# Import BeautifulSoup for parsing HTML
from bs4 import BeautifulSoup

# Asynchronously fetches the title and description from a web page
# Returns a dictionary with 'title' and 'description' keys
async def fetch_metadata(url: str) -> dict[str, str | None]:
    title = None
    description = None

    try:
        # Create an async HTTP client (follows redirects, 10s timeout)
        async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
            response = await client.get(url)  # Fetch the web page
            response.raise_for_status()  # Raise error if status is not 2xx

        # Parse the HTML content using BeautifulSoup and lxml parser
        soup = BeautifulSoup(response.text, "lxml")

        # Extract the <title> tag if present
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        # Extract the <meta name="description"> tag if present
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            description = meta_desc["content"].strip()

    except httpx.HTTPError:
        # Ignore HTTP errors (return None for title/description)
        pass

    return {"title": title, "description": description}
