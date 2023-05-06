import requests
import hashlib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_article_content(url):
    """
    Scrape the content of an article from a given URL.

    Parameters:
        url (str): The URL of the article.

    Returns:
        tuple: A tuple containing the heading and content of the article.
        The heading is a string and the content is a string of concatenated text.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the heading
    heading = soup.find('h1', {'class': 'article__title'})
    heading = heading.get_text(strip=True)

    # Get the content
    content_tags = soup.find_all('div', {'class': 'article-content'})
    content = ' '.join(' '.join(tag.stripped_strings) + ' ' for tag in content_tags).strip()

    return heading, content


def get_links():
    """
    Scrape the URLs of articles from the main page of TechCrunch.

    Returns:
        set: A set of URLs of articles.
    """
    # Set up Selenium options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode, without a visible browser window

    # Initialize the browser
    s = Service('path/to/chromedriver')  # Create a ChromeDriverService instance
    browser = webdriver.Chrome(service=s, options=options)  # Pass the ChromeDriverService instance

    # Navigate to the page
    browser.get("https://techcrunch.com/")

    # Get the HTML content
    html_content = browser.page_source

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the post-block__title__link anchor tags
    link_tags = soup.find_all('a', {'class': 'post-block__title__link'})

    # Extract the links
    links = set(tag['href'] for tag in link_tags)

    # Close the browser
    browser.quit()

    return links


def scrape_articles(base_url, links):
    """
    Scrape the content of multiple articles from a given set of URLs.

    Parameters:
        base_url (str): The base URL of the website.
        links (set): A set of article URLs.

    Returns:
        dict: A dictionary of article headings as keys and a tuple of article URL and content as values.
        The heading is a string, the URL is a string, and the content is a string of concatenated text.
    """
    articles = {}
    for link in links:
        full_url = base_url + link
        heading, content = get_article_content(full_url)
        articles[heading] = (full_url, content)

    return articles


def get_techcrunch_main_page_hash():
    """
    Compute the MD5 hash of the HTML content of the main page of TechCrunch.

    Returns:
        str: The MD5 hash of the HTML content of the main page of TechCrunch.
    """
    options = Options()
    options.add_argument("--headless")
    s = Service('path/to/chromedriver')
    browser = webdriver.Chrome(service=s, options=options)
    browser.get("https://techcrunch.com/")
    html_content = browser.page_source
    browser.quit()

    return hashlib.md5(html_content.encode('utf-8')).hexdigest()


def main():
    """
    Scrape the content of articles from the main page of TechCrunch.

    Returns:
        dict: A dictionary of article headings as keys and a tuple of article URL and content as values.
        The heading is a string, the URL is a string, and the content is a string of concatenated text.
    """
    base_url = "https://www.techcrunch.com"
    links = get_links()
    return scrape_articles(base_url, links)

if __name__ == "__main__":
    main()