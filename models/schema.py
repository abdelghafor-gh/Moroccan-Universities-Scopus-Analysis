from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Publication(Base):
    """Fact table for publications"""
    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    cited_by = Column(Integer)
    document_type = Column(String)
    source_title = Column(String)
    doi = Column(String)
    link = Column(String)
    
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
    publisher = Column(String)
    publication_type = Column(String)

class Author(Base):
    """Dimension table for authors"""
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    scopus_id = Column(String, unique=True)
    name = Column(String)
    h_index = Column(Integer)
    document_count = Column(Integer)
    citation_count = Column(Integer)

class Affiliation(Base):
    """Dimension table for affiliations"""
    __tablename__ = 'affiliations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    country = Column(String)
    scopus_id = Column(String, unique=True)
    type = Column(String)  # university, institute, etc.
