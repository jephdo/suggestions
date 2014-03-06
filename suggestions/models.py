from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    created = Column(DateTime, default=datetime.now)

    @classmethod
    def bulk_insert_tags(cls, query, tags):
        pass


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    value = Column(String(255))
    created = Column(DateTime, default=datetime.now)

    document_id = Column(Integer, ForeignKey('document.id'), nullable=False)

    def to_dict(self):
        return {self.name: self.value}


class TagClicks(Base):
    __tablename__ = 'tagclicks'

    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)
    created = Column(DateTime, default=datetime.now)

    # user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

def create_all():
    """
    Generate a sqlite database and populate it with the sample csv file
    as specified in the settings file.
    """
    import csv
    import random

    from sqlalchemy import create_engine

    from . import settings

    print('Starting a new sqlite database -- creating tables...')
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    conn = engine.connect()

    print('Loading .csv file into sqlite...')
    with open(settings.SAMPLE_CSV_FILE) as f:
        csv_reader = csv.reader(f, delimiter='\t')

        # python2 uses `next` and python3 uses `__next__`
        try:
            column_headers = csv_reader.next()
        except AttributeError:
            column_headers = csv_reader.__next__()

        rows = list(csv_reader)
        documents = [{'name':row[0]} for row in rows]
        conn.execute(Document.__table__.insert(), documents)

        tags = []
        for i, row in enumerate(rows):
            document_id = i + 1
            for n, cell in enumerate(row):
                if (1. / (n+1)) > random.random():
                    tag = {
                        'document_id': document_id, 
                        'name': column_headers[n],
                        'value': cell
                    }
                    tags.append(tag)

        conn.execute(Tag.__table__.insert(), tags)

    print('Finished generating database.')
