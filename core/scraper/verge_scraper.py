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

    # Get the heading, try two different class options
    heading = soup.find('h1', {'class': 'inline'})
    if not heading:
        heading = soup.find('h1', {'class': 'duet--article--feature-headline'})
    
    heading = heading.get_text(strip=True)

    # Get the content, combine the text within paragraph tags with the specified class
    content_tags = soup.find_all('p', {'class': 'duet--article--dangerously-set-cms-markup'})
    content = ' '.join(' '.join(tag.stripped_strings) + ' ' for tag in content_tags).strip()

    return heading, content


def get_links(): 
    """
    Scrape the article links from the main tech page of The Verge.

    Parameters:
        None.

    Returns:
        set: A set of article links that match the specified format.
    """
    # Set up Selenium options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode, without a visible browser window

    # Initialize the browser
    s = Service('path/to/chromedriver')  # Create a ChromeDriverService instance
    browser = webdriver.Chrome(service=s, options=options)  # Pass the ChromeDriverService instance

    # Navigate to the page
    browser.get("https://www.theverge.com/tech")

    # Get the HTML content
    html_content = browser.page_source

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the h2 tags
    h2_tags = soup.find_all('h2')

    # Extract links matching the specified format
    links = set()
    for h2 in h2_tags:
        link = h2.find('a')
        if link and link['href'].startswith('/2023/'):
            links.add(link['href'])

    # Close the browser
    browser.quit()

    return links


def scrape_articles(base_url, links):
    """
    Scrape the content of a set of articles specified in the input links.

    Parameters:
        base_url (str): The base URL of The Verge website.
        links (set): A set of article links that match the specified format.

    Returns:
        dict: A dictionary where the keys are the article headings, and the values
        are tuples containing the article URL and content.
    """
    articles = {}
    for link in links:
        full_url = base_url + link
        heading, content = get_article_content(full_url)
        articles[heading] = (full_url, content)

    return articles


def get_verge_main_page_hash():
    """
    Compute the hash of the main page of The Verge Tech.

    Parameters:
        None.

    Returns:
        str: The MD5 hash of the HTML content of the main page of The Verge Tech.
    """
    options = Options()
    options.add_argument("--headless")
    s = Service('path/to/chromedriver')
    browser = webdriver.Chrome(service=s, options=options)
    browser.get("https://www.theverge.com/tech")
    html_content = browser.page_source
    browser.quit()

    return hashlib.md5(html_content.encode('utf-8')).hexdigest()


def main(): 
    """
    The main function that calls the get_links() and scrape_articles() functions
    and returns the scraped articles.

    Parameters:
        None.

    Returns:
        dict: A dictionary where the keys are the article headings, and the values
        are tuples containing the article URL and content.
    """
    base_url = "https://www.theverge.com"
    links = get_links()
    return scrape_articles(base_url, links)

if __name__ == "__main__":
    main()