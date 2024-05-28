from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # SQLite URI
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.id}>'

@app.route('/')
def index():
    books = Book.query.order_by(Book.id).all()
    return render_template("index.html", books=books)

@app.route('/add', methods=["POST", "GET"])
def add_book():
    if request.method == 'POST':
        new_book_name = request.form['title']
        new_author = request.form['author']
        new_genre = request.form['genre']
        new_price = request.form['price']
        new_book = Book(title=new_book_name, author=new_author, genre=new_genre, price=new_price)
        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    
    return render_template("add_book.html")

@app.route('/delete/<int:id>', methods=["POST", "GET"])
def delete_book(id):
    book_to_delete = Book.query.get_or_404(id)
    if request.method == 'POST':
        try:
            db.session.delete(book_to_delete)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    
    return render_template("delete_book.html", book=book_to_delete)

@app.route('/edit/<int:id>', methods=["POST", "GET"])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.price = request.form['price']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    else:
        return render_template('edit_book.html', book=book)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
