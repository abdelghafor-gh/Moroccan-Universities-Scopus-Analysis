from sqlalchemy import Column, Integer, BigInteger, String, Float, Date, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Publication(Base):
    """Fact table for publications"""
    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    volume = Column(String)
    issue = Column(String)
    document_type = Column(String)
    source_title = Column(String)
    doi = Column(String)
    link = Column(String)
    pubmed_id = Column(String)
    language = Column(String)
    
    # Foreign Keys
    journal_id = Column(Integer, ForeignKey('journals.id'))
    author_id = Column(Integer, ForeignKey('authors.id'))
    affiliation_id = Column(Integer, ForeignKey('affiliations.id'))

class Journal(Base):
    """Dimension table for journals"""
    __tablename__ = 'journals'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    issn = Column(String)
    type = Column(String)
    rank = Column(Integer)
    sjr = Column(Float)
    publisher = Column(String)
    areas = Column(String)


class Author(Base):
    """Dimension table for authors"""
    __tablename__ = 'authors'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    
class Affiliation(Base):
    """Dimension table for affiliations"""
    __tablename__ = 'affiliations'


    id = Column(Integer, primary_key=True)
    affiliation = Column("Affiliation", String)
    abbreviation = Column("Abbreviation", String)
    city = Column("City", String)
    # country = Column(String)
    # type = Column(String)  # university, institute, etc.
