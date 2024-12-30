from sqlalchemy import Column, Integer, BigInteger, String, Float, Date, ForeignKey, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

metadata = MetaData()
Base = declarative_base(metadata=metadata)

class Publication(Base):
    """Fact table for publications from Moroccan Universities in Scopus.

    This table stores detailed information about academic publications, including their
    metadata and relationships to authors, journals, and affiliations.

    Attributes:
        id (BigInteger): Primary key for the publication.
        Title (String): Full title of the publication.
        Year (Integer): Publication year.
        Volume (String): Volume number of the publication.
        Issue (String): Issue number of the publication.
        ISSN (String): International Standard Serial Number of the journal.
        Source_Title (String): Title of the source journal/conference.
        Document_Type (String): Type of document (e.g., article, book series, conference paper).
        DOI (String): Digital Object Identifier.
        Link (String): URL to access the publication.
        PubMed_ID (String): PubMed database identifier.
        Original_Language (String): Original language of the publication.
        author_id (BigInteger): Foreign key to authors table.
        affiliation_id (Integer): Foreign key to affiliations table.
    """
    __tablename__ = 'publications'

    id = Column(BigInteger, primary_key=True)
    Title = Column("Title", String)
    Year = Column("Year", Integer)
    Volume = Column("Volume", String)
    Issue = Column("Issue", String)
    ISSN = Column("ISSN", String)
    Source_Title = Column("Source Title", String, key="Source Title")
    Document_Type = Column("Document Type", String, key="Document Type")
    DOI = Column("DOI", String, key="DOI")
    Link = Column("Link", String)
    PubMed_ID = Column("PubMed ID", String, key="PubMed ID")
    Original_Language = Column("Language of Original Document", String, key="Language of Original Document")
    
    # Foreign Keys
    # ISSN = Column("ISSN", String, ForeignKey('journals.ISSN'), key="ISSN")
    author_id = Column("Author ID", BigInteger, ForeignKey('authors.id'), key="Author ID")
    affiliation_id = Column("Affiliation ID", Integer, ForeignKey('affiliations.id'), key="Affiliation ID")


class Journal(Base):
    """Dimension table for academic journals and their metrics.

    This table contains information about journals where the publications appear,
    including their impact metrics and classification.

    Attributes:
        id (BigInteger): Journal identifier.
        Title (String): Full name of the journal.
        ISSN (String): Primary key - International Standard Serial Number.
        Type (String): Type of the journal.
        Rank (Integer): Journal ranking.
        SJR (Float): SCImago Journal Rank indicator.
        Publisher (String): Name of the journal publisher.
        Areas (String): Research areas covered by the journal.
    """
    __tablename__ = 'journals'

    id = Column(BigInteger)
    Title = Column("Title", String)
    ISSN = Column("ISSN", String, primary_key=True)
    Type = Column("Type", String)
    Rank = Column("Rank", Integer)
    SJR = Column("SJR", Float)
    Publisher = Column("Publisher", String)
    Categories = Column("Categories", String)


class JournalCategory(Base):
    """Journal Category dimension table"""
    __tablename__ = "journal_categories"

    id = Column("id", Integer, primary_key=True)
    ISSN = Column("ISSN", String, ForeignKey("journals.ISSN"))
    Category = Column("Category", String)


class Author(Base):
    """Dimension table for publication authors.

    This table stores information about authors who have published papers
    affiliated with Moroccan Universities.

    Attributes:
        id (BigInteger): Primary key - Unique identifier for the author.
        Name (String): Full name of the author.
        affiliation_id (Integer): Foreign key to affiliations table.
    """
    __tablename__ = 'authors'

    id = Column(BigInteger, primary_key=True)
    Name = Column(String)

    affiliation_id = Column(Integer, ForeignKey('affiliations.id'))


class Affiliation(Base):
    """Dimension table for institutional affiliations.

    This table contains information about the academic institutions and their
    properties, focusing on Moroccan Universities and research centers.

    Attributes:
        id (Integer): Primary key - Unique identifier for the affiliation.
        Affiliation (String): Full name of the affiliated institution.
        Abbreviation (String): Common abbreviation or acronym for the institution.
        University (String): Name of the university.
        City (String): City where the institution is located.
        Type (String): Type of institution (e.g., university, institute, school).
    """
    __tablename__ = 'affiliations'

    id = Column(Integer, primary_key=True)
    Affiliation = Column(String)
    Abbreviation = Column(String)
    University = Column(String)
    City = Column(String)
    Type = Column(String)  # university, institute, etc.
