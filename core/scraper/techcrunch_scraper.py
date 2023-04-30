import requests
import hashlib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Function to get article heading and content
def get_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the heading
    heading = soup.find('h1', {'class': 'article__title'})
    heading = heading.get_text(strip=True)

    # Get the content
    content_tags = soup.find_all('div', {'class': 'article-content'})
    content = ' '.join(' '.join(tag.stripped_strings) + ' ' for tag in content_tags).strip()

    return heading, content

# Function to get links from the main TechCrunch page
def get_links():
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

# Function to scrape article content for a set of links
def scrape_articles(base_url, links):
    articles = {}
    for link in links:
        full_url = base_url + link
        heading, content = get_article_content(full_url)
        articles[heading] = (full_url, content)

    return articles

# Function to compute the hash of the main page of TechCrunch
def get_techcrunch_main_page_hash():
    options = Options()
    options.add_argument("--headless")
    s = Service('path/to/chromedriver')
    browser = webdriver.Chrome(service=s, options=options)
    browser.get("https://techcrunch.com/")
    html_content = browser.page_source
    browser.quit()

    return hashlib.md5(html_content.encode('utf-8')).hexdigest()

# Main function
def main():
    base_url = "https://www.techcrunch.com"
    links = get_links()
    return scrape_articles(base_url, links)

if __name__ == "__main__":
    main()