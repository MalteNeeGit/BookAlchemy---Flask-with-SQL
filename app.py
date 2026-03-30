from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book
from datetime import datetime

app = Flask(__name__)

#Database URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

#Verbindet Flask app mit dem Flask-SQL-Alchemy code
db.init_app(app)

#Tabbellen erstellen, die in data_models definiert sind:
# nach dem verwenden auskommentieren
"""with app.app_context():
  db.create_all()"""


@app.route('/', methods=["GET"])
def home():
    #wenn du url so aussieht localhost:5000/?sort=title
    sort = request.args.get('sort')  # liest ?sort=... aus der URL

    #Suchfunktion
    user_search = request.args.get('q')

    # erstmal nur die Basis-Query ohne .all()
    query = Book.query

    # dann Filter draufpacken wenn gesucht wird
    if user_search:
        query = query.filter(Book.title.like(f"%{user_search}%"))

    # dann Sortierung draufpacken
    if sort == 'author':
        query = query.join(Author).order_by(Author.name)
    else:
        query = query.order_by(Book.title)

    # erst am Ende ausführen
    books = query.all()

    return render_template("home.html", books=books)

@app.route('/add_author', methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        name = request.form.get('name')
        birth_date_str = request.form.get('birthdate')
        date_of_death_str = request.form.get('date_of_death')

        #date_obj umwandeln:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()

        date_of_death = None
        if date_of_death_str:
            date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date()

        #author erstellen und in db speichern:
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()

        return render_template('add_author.html', success=True)

    return render_template('add_author.html')

@app.route('/add_book', methods=["GET", "POST"])
def add_book():
    #authoren holen für die author id:
    authors = Author.query.all()

    if request.method == "POST":
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year_str = request.form.get('publication_year')
        author_id = request.form.get('author_id')

        #publication year umwandeln
        publication_year = datetime.strptime(publication_year_str,'%Y-%m-%d').date()

        #neues buch anlegen:
        new_book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()

        #authors=authors mitgeben, damit wir über jinja im add_book darauf zugreifen können
        return render_template('add_book.html', success=True, authors=authors)

    return render_template('add_book.html', authors=authors)

@app.route('/book/<int:book_id>/delete', methods=["POST"])
def delete_book(book_id):
    book_to_search = Book.query.get(book_id)

    if book_to_search:
        #Author holen bevor wir löschen:
        author = book_to_search.author

        db.session.delete(book_to_search)
        db.session.commit()

        if not author.books:
            db.session.delete(author)
            db.session.commit()

        return redirect(url_for('home'))

    else:
        return "Buch nicht gefunden", 404




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)