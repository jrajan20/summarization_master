from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def _parse_html_content(html_content):
    """
    Helper function to parse HTML and extract title and text content.
    Returns a tuple of (title, text).
    """
    soup = BeautifulSoup(html_content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return title, text


def fetch_website_contents_simple(url, timeout=30):
    """
    Fetch website contents using simple requests (no JavaScript execution).
    Fast but won't work for JavaScript-rendered content.
    """
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        title, text = _parse_html_content(response.content)
        return (title + "\n\n" + text)[:2_000]
    except Exception as e:
        raise Exception(f"Simple fetch failed: {str(e)}")


def fetch_website_contents_js(url, timeout=30000):
    """
    Fetch website contents using Playwright (executes JavaScript).
    Slower but works for modern JavaScript-rendered sites.
    
    Args:
        url: The URL to fetch
        timeout: Timeout in milliseconds (default: 30 seconds)
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(timeout)
            
            try:
                # Use 'load' instead of 'networkidle' - more reliable and faster
                page.goto(url, wait_until='load', timeout=timeout)
                # Give JavaScript a moment to render
                page.wait_for_timeout(2000)
                html_content = page.content()
            finally:
                browser.close()
            
            title, text = _parse_html_content(html_content)
            return (title + "\n\n" + text)[:2_000]
    except PlaywrightTimeoutError:
        raise Exception(f"Playwright fetch timed out after {timeout}ms")
    except Exception as e:
        raise Exception(f"Playwright fetch failed: {str(e)}")


def fetch_website_contents(url, timeout=30):
    """
    Intelligently fetch website contents using a hybrid approach:
    1. Try simple requests first (fast)
    2. If content is too short, fall back to Playwright (handles JavaScript)
    
    Returns the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit.
    
    Args:
        url: The URL to fetch
        timeout: Timeout in seconds for simple requests, milliseconds for Playwright
    """
    try:
        content = fetch_website_contents_simple(url, timeout=timeout)
        
        # If content is suspiciously short (likely JavaScript-rendered), use Playwright
        if len(content) < 500:
            try:
                content = fetch_website_contents_js(url, timeout=timeout * 1000)
            except Exception as js_error:
                # If Playwright fails, return the simple content anyway
                # (better than nothing, and includes the error info)
                pass
        
        return content
    except Exception as simple_error:
        # If simple fetch completely fails, try Playwright as fallback
        try:
            return fetch_website_contents_js(url, timeout=timeout * 1000)
        except Exception as js_error:
            # Both methods failed, raise the original simple error
            raise simple_error



def fetch_website_links(url):
    """
    Return the links on the webiste at the given url
    I realize this is inefficient as we're parsing twice! This is to keep the code in the lab simple.
    Feel free to use a class and optimize it!
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]
