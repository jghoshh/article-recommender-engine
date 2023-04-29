import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  # Import ChromeDriverService

# Function to get article heading and content
def get_article_content(url):
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

# Function to get links from the main tech page
def get_links(): 
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

# Function to scrape article content for a set of links
def scrape_articles(base_url, links):
    articles = {}
    for link in links:
        full_url = base_url + link
        heading, content = get_article_content(full_url)
        articles[heading] = (full_url, content)

    return articles

# Main function 
def main(): 
    base_url = "https://www.theverge.com"
    links = get_links()
    return scrape_articles(base_url, links)

if __name__ == "__main__":
    main()