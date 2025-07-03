from flask import Flask
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(200), unique=False, nullable=False)
    author = db.Column(db.String(200), unique=False, nullable=False)
    publisher = db.Column(db.String(200), unique=False, nullable=False)

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"


@app.route('/')
def index():
    return 'Hello!'

@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {
            'title': book.book_name,
            'author': book.author,
            'publisher': book.publisher
            }

        output.append(book_data)
        

    return {"books": output}

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "not found"}, 404
    db.session.delete(book)
    db.session.commit()
    return {"message": "Book deleted successfully."}, 200