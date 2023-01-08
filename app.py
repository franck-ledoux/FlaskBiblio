from flask import Flask, jsonify, abort, request, Response, render_template
from library import Library

# ==============================================================================
# #Create the flask server object
# ==============================================================================
app = Flask(__name__)

# ==============================================================================
# Create the library object with 3 books
# ==============================================================================
lib = Library()
lib.addBook("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 12301)
lib.addBook("Da Vinci Code", "D. Brown", 11244)
lib.addBook("Twenty Thousand Leagues Under The Sea", "J. Verne", 23900)

# ==============================================================================
# Handle abort message
# ==============================================================================
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


# ==============================================================================
# Routes definition to expose a REST API
# ==============================================================================

@app.route('/')
@app.route('/library/', methods=['GET'])
def all_book():
    response = lib.serialize()
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

@app.route('/library/<int:isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    books = lib.getBook(isbn)
    if books:
        print(books[0].serialize())
        response = jsonify(books[0].serialize())
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        response.status = 201
        return response
    else:
        abort(404, description="No book with ISBN ")


if __name__ == '__main__':
    app.run()
