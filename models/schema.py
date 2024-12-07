from sqlalchemy import Column, Integer, BigInteger, String, Float, Date, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Publication(Base):
    """Fact table for publications"""
    __tablename__ = 'publications'

    id = Column(BigInteger, primary_key=True)
    Title = Column("Title", String)
    Year = Column("Year", Integer)
    Volume = Column("Volume", String)
    Issue = Column("Issue", String)
    ISSN = Column("ISSN", String)
    source_title = Column("Source Title", String, key="Source Title")
    document_type = Column("Document Type", String, key="Document Type")
    DOI = Column("DOI", String, key="DOI")
    Link = Column("Link", String)
    pubmed_id = Column("PubMed ID", String, key="PubMed ID")
    language = Column("Language of Original Document", String, key="Language of Original Document")
    
    # Foreign Keys
    # ISSN = Column("ISSN", String, ForeignKey('journals.ISSN'), key="ISSN")
    author_id = Column("Author ID", BigInteger, ForeignKey('authors.id'), key="Author ID")
    affiliation_id = Column("Affiliation ID", Integer, ForeignKey('affiliations.id'), key="Affiliation ID")


class Journal(Base):
    """Dimension table for journals"""
    __tablename__ = 'journals'

    id = Column(BigInteger)
    Title = Column("Title", String)
    ISSN = Column("ISSN", String, primary_key=True)
    Type = Column("Type", String)
    Rank = Column("Rank", Integer)
    SJR = Column("SJR", Float)
    Publisher = Column("Publisher", String)
    Areas = Column("Areas", String)


class Author(Base):
    """Dimension table for authors"""
    __tablename__ = 'authors'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    
class Affiliation(Base):
    """Dimension table for affiliations"""
    __tablename__ = 'affiliations'

    id = Column(Integer, primary_key=True)
    Affiliation = Column(String)
    Abbreviation = Column(String)
    University = Column(String)
    City = Column(String)
    # affiliation = Column("Affiliation", String)
    # abbreviation = Column("Abbreviation", String)
    # university = Column("University", String)
    # city = Column("City", String)
    # country = Column(String)
    # type = Column(String)  # university, institute, etc.
