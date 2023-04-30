from apscheduler.schedulers.blocking import BlockingScheduler
from verge_scraper import main as scrape_verge, get_verge_main_page_hash
from techcrunch_scraper import main as scrape_techcrunch, get_techcrunch_main_page_hash
import redis

# Initialize Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

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
    scheduler.add_job(monitor_and_scrape, 'interval', seconds=30)  # Execute monitor_and_scrape every 5 minutes
    scheduler.start()

