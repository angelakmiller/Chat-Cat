import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import pdfkit

def crawl_and_convert(url, base_url):
    """Crawls a website and converts each page to PDF."""

    visited = set()
    pdfs = []

    def crawl(url):
        if url in visited:
            return
        visited.add(url)

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {url}: {e}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        # Convert the page to PDF
        try:
            pdf_name = f"{urlparse(url).path.replace('/', '_')}.pdf"
            pdfkit.from_url(url, pdf_name)
            pdfs.append(pdf_name)
            print(f"Converted {url} to {pdf_name}")
        except Exception as e:
            print(f"Error converting {url} to PDF: {e}")

        # Find all links on the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/'):
                href = urljoin(base_url, href)
            if href.startswith(base_url) and href not in visited:
                crawl(href)

    crawl(url)
    return pdfs

if __name__ == "__main__":
    base_url = "https://profiles.arizona.edu/person/pratiksatam"  # Replace with the website you want to crawl
    pdfs = crawl_and_convert(base_url, base_url)
    print("All PDFs generated:", pdfs)
