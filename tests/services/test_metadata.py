import respx
from httpx import Response

from app.services import metadata


@respx.mock
async def test_fetch_metadata_success():
    url = "https://example.com"
    html = """
    <html>
      <head>
        <title>Test Title</title>
        <meta name="description" content="Test description here." />
      </head>
      <body></body>
    </html>
    """
    respx.get(url).mock(return_value=Response(200, text=html))
    result = await metadata.fetch_metadata(url)
    assert result["title"] == "Test Title"
    assert result["description"] == "Test description here."


@respx.mock
async def test_fetch_metadata_no_description():
    url = "https://example.com"
    html = """
    <html><head><title>Only Title</title></head><body></body></html>
    """
    respx.get(url).mock(return_value=Response(200, text=html))
    result = await metadata.fetch_metadata(url)
    assert result["title"] == "Only Title"
    assert result["description"] is None


@respx.mock
async def test_fetch_metadata_http_error():
    url = "https://example.com"
    respx.get(url).mock(return_value=Response(404))
    result = await metadata.fetch_metadata(url)
    assert result["title"] is None
    assert result["description"] is None
