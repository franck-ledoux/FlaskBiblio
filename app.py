from flask import Flask, jsonify, abort, request, Response, render_template, make_response
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
    response = make_response(lib.serialize())
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

@app.route('/library/', methods=['POST'])
def add_book():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        if "isbn" in json and "author" in json and "title" in json:
            lib.addBook(json["title"], json["author"], json["isbn"])
            response = make_response("book added")
            response.status =201
            response.location = "library/"+str(json["isbn"])
            return response
        else:
            return {"message": "wrong format"}
    else:
        return {"message": "Content-Type not supported!"}

@app.route('/library/<int:isbn>/<string:author>/<string:title>', methods=['PUT'])
def add_book2(isbn, author, title):
    if not lib.getBook(isbn):
        lib.addBook(title, author, isbn)
        response = make_response(jsonify(lib.getBook(isbn)[0].serialize()))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        response.status = 201
        response.headers['location'] = '/library/'+str(isbn)
        return response
    return "book in lib", 304 # not modified


@app.route('/library/<int:isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    books = lib.getBook(isbn)
    if books:
        print(books[0].serialize())
        response = make_response(jsonify(books[0].serialize()))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        response.status = 201
        return response
    else:
        abort(404, description="No book with ISBN ")

@app.route('/library/<int:isbn>', methods=['DELETE'])
def del_book_by_isbn(isbn):
    done = lib.delBook(isbn)
    if done:
        response = make_response("Book removed")
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        response.status = 204
        return response
    else:
        abort(404, description="No book with ISBN ")


if __name__ == '__main__':
    app.run()
