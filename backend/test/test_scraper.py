import unittest
from models import *
from config import settings
from recipes_scraper import *

class TestScraper(unittest.TestCase):

    def test_scraper(self):
        reddit_scraper = RedditScraper(settings.reddit_client_id, settings.reddit_client_secret)
        reddit_post = reddit_scraper.get_hot_post()
        self.assertIsInstance(reddit_post, RedditPost)
        self.assertIsInstance(reddit_post.id, str)
        self.assertIsInstance(reddit_post.title, str)
        self.assertIsInstance(reddit_post.url, str)
        self.assertIsInstance(reddit_post.author, str)
        self.assertIsInstance(reddit_post.text, str)
    
    def test_db(self):
        reddit_scraper = RedditScraper(settings.reddit_client_id, settings.reddit_client_secret)
        reddit_post = reddit_scraper.get_hot_post()
        reddit_post_db = RedditPostDB(settings.database_url)
        reddit_post_db.insert(reddit_post)
        reddit_post_db.close()
        reddit_post_db = RedditPostDB(settings.database_url)
        reddit_post_db.delete(reddit_post)
        reddit_post_db.close()

if __name__ == '__main__':
    unittest.main()