# instantiate a reddit instance
import praw
from tqdm import tqdm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from config import settings
from models import *

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
                id=submission.id,
                title=submission.title,
                text=submission.selftext or op_comment,
                url=submission.url,
                author=submission.author.name,

            )

    def get_hot_post(self) -> RedditPost:
        return next(self.get_hot_posts(limit=1))
    

class RedditPostDB:
    def __init__(self, connection_string, drop_existing=False) -> None:
        self.engine = create_engine(connection_string)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.conn = self.engine.connect()

        if drop_existing:
            self.drop_table()
        self.create_table()

    def drop_table(self):
        self.c.execute("DROP TABLE IF EXISTS reddit_posts")
        self.conn.commit()
        

    def create_table(self):
        Base.metadata.create_all(self.engine)
        self.conn.commit()

    def get_all(self) -> list[RedditPost]:
        return self.session.query(RedditPost).all()
    
    def close(self):
        self.session.close()

    def insert(self, reddit_post, duplicate='ignore'):
        if duplicate == 'ignore':
            try:
                self.session.add(reddit_post)
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
        elif duplicate == 'replace':
            self.session.merge(reddit_post)
            self.session.commit()
        else:
            raise ValueError(f"Duplicate value {duplicate} not recognized")
        
    def delete(self, reddit_post):
        self.session.query(RedditPost).filter(RedditPost.id == reddit_post.id).delete()
        self.session.commit()

if __name__ == "__main__":

    reddit_scraper = RedditScraper(settings.reddit_client_id, settings.reddit_client_secret)
    reddit_db = RedditPostDB(settings.database_url , )
    
    for i, reddit_post  in tqdm(enumerate(reddit_scraper.get_hot_posts(limit=10))):
        reddit_db.insert(reddit_post, duplicate='replace')

