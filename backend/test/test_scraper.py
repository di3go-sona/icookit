import unittest
import recipes_scraper
import os

from config import settings

class TestStringMethods(unittest.TestCase):

    def test_reddit_scraper(self):
        reddit_scraper = recipes_scraper.RedditScraper(
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_client_secret
        )

            

if __name__ == '__main__':
    unittest.main()