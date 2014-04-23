# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import Frames, db_connect, create_frames_table
class FramescrapperPipeline(object):

    def __init__(self):
        """
        Initializes the database connection and
        sessionmaker.
        Creates frames table.
        """
        engine = db_connect()
        create_frames_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """
        saves frames into the database
        """

        session = self.Session()
        frame = Frames(**item)

        try:
            session.add(frame)
            session.commit()

        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
