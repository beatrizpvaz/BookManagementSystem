from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import BookForm, AddReview
from . import directory
from ..models import Book, User
from .. import db

import requests

@directory.route('/directory', methods=['GET', 'POST'])
@login_required
def list_books():
    """
    List all books
    """

    books = Book.query.all()

    #NEED TO ADD TEMPLATE
    return render_template('directory/directory.html',
                           books=books, title="Books")

@directory.route('/directory/add', methods=['GET', 'POST'])
@login_required
def add_books():
    """
    Add new books to the db
    """
    add_book = True

    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author = form.author.data,
            publisher = form.publisher.data,
            year = form.year.data,
            logged_by = form.logged_by.data,
            review = form.review.data
        )
                        
        try:
            db.session.add(book)
            db.session.commit()
            flash('Book added to the directory ', 'success')
        except:
            # in case department name already exists
            flash('Book is already registered', 'error')

        #NEED TO ADD TEMPLATE
        return redirect(url_for('directory.list_books'))

    # #NEED TO ADD TEMPLATE
    return render_template('directory/book.html', action="Add",
                           add_books=add_book, form=form,
                           title="Add Book")

@directory.route('/directory/edit/<int:id>/<string:action>', methods=['GET', 'POST'])
@login_required
def edit_books(id, action):
    """
    Edit books in the database
    """
    add_book = False
    # add_review = False

    book = Book.query.get_or_404(id)
    if (action=='add_review'):
        form= AddReview()
        if form.validate_on_submit():
            form.populate_obj(book)
            db.session.commit()
            flash("You have added a review {}", book.review)

            return redirect(url_for('directory.book_info', id = id))

    else:
        form = BookForm(obj = book)
        if form.validate_on_submit():
            form.populate_obj(book)
            db.session.commit()

            flash("You have edited the book {}", book.title)

            # redirect to the books directory
            return redirect(url_for('directory.list_books'))


    return render_template('directory/book.html', action="Edit",
                           add_books=add_book, form=form,
                           title="Edit Book")

@directory.route('/directory/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_books(id):
    """
    Delete book from the database
    """

    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('You have successfully deleted the book')

    # redirect to the roles page
    return redirect(url_for('directory.list_books'))

@directory.route('/directory/bookinfo/<int:id>', methods = ['GET', 'POST'])
@login_required
def book_info(id):
    """
    Goes to each books individual page
    """
    book = Book.query.get_or_404(id)

    return render_template('directory/bookpage.html', 
                            book_db = book,
                            books_result=requests.get("https://www.googleapis.com/books/v1/volumes?q="
                                +book.title+"+inauthor:"+book.author
                                +"&key=AIzaSyAQAR3-9hTT-O7VYf022aaO4lshg0q2vHU").json(),
                            title="Books")

