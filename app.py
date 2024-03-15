from flask import Flask, jsonify, redirect, render_template, request, url_for

from database import (
    add_review_to_db,
    load_authors_from_db,
    load_book_details,
    load_reviews_from_db,
)

app = Flask(__name__)

# Display all reviews for particular book on that book's reviews page
# Add word filter for reviews
# Add pagination for reviews (that thing with the pages listed (< 1 2 3 >)) OR infinite scroll
# Search bar for books
# Sorting books and reviews
# Getting book info from some API
# Add user login
# Add captcha to form
# Add admin login
# Rating for each book in review
# Like reviews


@app.errorhandler(403)
def forbidden(error):
  return render_template(
      'error.html',
      error_code=403,
      error_message='Forbidden, classified information'), 403


@app.errorhandler(404)
def page_not_found(error):
  return render_template(
      'error.html',
      error_code=404,
      error_message=
      'Not Found, someone typed something wrong and it was probably you.'), 404


@app.errorhandler(405)
def method_not_allowed(error):
  return render_template(
      'error.html',
      error_code=405,
      error_message='Method Not Allowed, do better sweetie.'), 405


@app.route("/")
def home():
  authors = load_authors_from_db()
  return render_template('home.html', authors=authors)


@app.route("/new")
def new():
  return render_template('new.html')


@app.route("/about")
def about():
  return render_template('about.html', title='About')


@app.route("/api/authors")
def list():
  api_authors = load_authors_from_db()
  return jsonify(api_authors)


@app.route("/book/<id>")
def details(id):
  book = load_book_details(id)
  if not book:
    return "Not Found", 404

  return render_template('book.html', book=book)
  #return jsonify(author)


@app.route("/book/<id>/review", methods=['post'])
def create_review(id):
  data = request.form
  book = load_book_details(id)
  add_review_to_db(id, data)
  # return render_template('review.html', review=data, book=book)
  return redirect(url_for('review_submitted', id=id))


@app.route("/book/<id>/review/submitted")
def review_submitted(id):
  book = load_book_details(id)
  return render_template('review.html', book=book)


# @app.route("/book/<id>/reviews")
# def load_reviews(id):
#     book = load_book_details(id)
#     reviews_data = load_reviews_from_db(id)

#     fetched_reviews = []
#     for row in reviews_data:
#         fetched_reviews.append(row._asdict())

#     if not fetched_reviews:
#         return "No reviews found for this book"
#     else:
#       return render_template('reviews.html', reviews_data=fetched_reviews, book=book)
# return jsonify(reviews_data)


@app.route("/book/<id>/reviews")
def load_reviews(id):
  book = load_book_details(id)
  reviews_data = load_reviews_from_db(id)

  # If load_reviews_from_db returned None, meaning there are no reviews
  if reviews_data is None:
    return "No reviews found for this book", 404
  else:
    # Since reviews_data is a list of dictionaries, we can pass it directly to the template
    return render_template('reviews.html', reviews_data=reviews_data, book=book)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
