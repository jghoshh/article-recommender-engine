from apscheduler.schedulers.blocking import BlockingScheduler
from verge_scraper import main as scrape_verge, get_verge_main_page_hash
from techcrunch_scraper import main as scrape_techcrunch, get_techcrunch_main_page_hash
import redislite

# Create a Redis configuration file with AOF persistence enabled
config_file = 'redis.conf'
with open(config_file, 'w') as f:
    f.write('appendonly yes\n')

# Initialize Redis connection
# We use Redis to store the hashes of the html content of TechCrunch and The Verge
redis_client = redislite.Redis(serverconfig={"appendonly": "yes"})

# Function to monitor and scrape the main pages of 
def monitor_and_scrape():

    def check_verge():
        new_hash = get_verge_main_page_hash()
        old_hash = redis_client.get("verge_hash")
        if old_hash is None or new_hash != old_hash.decode('utf-8'):
            redis_client.set("verge_hash", new_hash)
            return True
        return False

    def check_techcrunch():
        new_hash = get_techcrunch_main_page_hash()
        old_hash = redis_client.get("techcrunch_hash")
        if old_hash is None or new_hash != old_hash.decode('utf-8'):
            redis_client.set("techcrunch_hash", new_hash)
            return True
        return False

    if check_verge():
        print("Scraping new articles from The Verge")
        articles = scrape_verge()
        # Process the articles here, e.g., send notifications or store them in a database

    if check_techcrunch():
        print("Scraping new articles from TechCrunch")
        articles = scrape_techcrunch()
        # Process the articles here, e.g., send notifications or store them in a database

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(monitor_and_scrape, 'interval', minutes=5)  # Execute monitor_and_scrape every 5 minutes
    scheduler.start() 