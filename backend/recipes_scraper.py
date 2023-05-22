# instantiate a reddit instance
import praw
import time
import os 
from tqdm import tqdm
from dataclasses import dataclass
import sqlite3
from config import settings

@dataclass
class RedditPost:
    title: str
    text: str
    id: str
    url: str
    author: str
    op_comment: str 

class RedditScraper:
    user_agent = "Comment Extraction (by u/USERNAME)"
    def __init__(self, client_id, client_secret) -> None:

        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=self.user_agent
            )
        self.subreddit = self.reddit.subreddit('recipes')

    def get_hot_posts(self, limit=100):
        hot_posts = self.subreddit.hot(limit=limit)
        for submission in hot_posts:
            op_comment = None
            for comment in submission.comments:
                if isinstance(comment, praw.models.Comment):

                    if comment.is_submitter:
                        op_comment = comment.body
                        break
            yield RedditPost(
                title=submission.title,
                text=submission.selftext,
                id=submission.id,
                url=submission.url,
                author=submission.author.name,
                op_comment=op_comment
            )

    def get_hot_post(self) -> RedditPost:
        return next(self.get_hot_posts(limit=1))
    

class RedditPostDB:
    def __init__(self, connection_string, drop_existing=False) -> None:
        self.conn = sqlite3.connect(connection_string)
        self.c = self.conn.cursor()
       
        if drop_existing:
            self.drop_table()
        self.create_table()

    def drop_table(self):
        self.c.execute('''DROP TABLE IF EXISTS reddit_posts''')
        self.conn.commit()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS reddit_posts
                (title text, text text, id text PRIMARY KEY, url text, author text, op_comment text)''')
        self.conn.commit()

    def insert_one(self, reddit_post):
        try:
            self.c.execute("INSERT INTO reddit_posts VALUES (?, ?, ?, ?, ?, ?)", (reddit_post.title, reddit_post.text, reddit_post.id, reddit_post.url, reddit_post.author, reddit_post.op_comment))
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback()
            print(f"Skipping duplicate post: {reddit_post.id}")

if __name__ == "__main__":


    # reddit_conf = {
    #     "client_id": os.environ["ICOOKIT_REDDIT_USER_ID"],
    #     "client_secret": os.environ["ICOOKIT_REDDIT_USER_SECRET"],
    #     "user_agent": "Comment Extraction (by u/USERNAME)",
    # }

    reddit_scraper = RedditScraper(settings.reddit_user_id, settings.reddit_user_secret)
    reddit_db = RedditPostDB("reddit.db", drop_existing=True)
    

    for i, reddit_post  in tqdm(enumerate(reddit_scraper.get_hot_posts(limit=100))):
        reddit_db.insert_one(reddit_post)

