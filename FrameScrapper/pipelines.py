# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import Frames, db_connect, create_frames_table

class FramescrapperPipeline(object):

    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):

        msg = '%%s %s pipeline step' %(self.Session__class__.__name__)

        if self.__class__ in spider.pipeline:
            spider.log(msg % 'executing', level=log.DEBUG)
            return process_item_method(self, item, spider)

        else:
            spider.log(msg % 'skipping', level=log.DEBUG)






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
