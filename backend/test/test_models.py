import unittest
from models import *
from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestModels(unittest.TestCase):

    def test_connection (self):
        engine = create_engine(settings.database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.close()

    def test_create_table (self):
        engine = create_engine(settings.database_url)
        Base.metadata.create_all(engine)
    
    def test_insert (self):
        engine = create_engine(settings.database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.query(RedditPost).filter(RedditPost.id == 'test').delete()
        session.add(RedditPost(title='test', text='test', id='test', url='test', author='test'))
        session.commit()
        session.query(RedditPost).filter(RedditPost.id == 'test').delete()
        session.commit()
        session.close()

if __name__ == '__main__':
    unittest.main()