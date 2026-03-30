from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey

#Das ist eine Klasse
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date)
    date_of_death = Column(Date)

    def __repr__(self):
        return f"Author name: {self.name} was born {self.birth_date}"

    def __str__(self):
        return self.name

class Book(db.Model):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String)
    title = Column(String, nullable=False)
    publication_year = Column(Date)

    #FOREIGN KEY um book mit author zu verbinden:
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    #realtionship erstellen:
    author = db.relationship('Author', backref='books')

    def __repr__(self):
        return f"Book name: {self.title} from the year {self.publication_year}"

    def __str__(self):
        return self.title


