from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import BookForm
from . import directory
from ..models import Book, User
from .. import db

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
                           add_book=add_book, form=form,
                           title="Add Book")

@directory.route('/directory/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_books(id):
    """
    Edit books in the database
    """

    add_book = True

    book = Book.query.get_or_404(id)
    form = BookForm(object = book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.publisher = form.publisher.data
        book.year = form.year.data
        book.review = form.review.data
        book.logged_by = form.logged_by.data

        db.session.add(book)
        db.session.commit()
        flash("You have edited the book {}", book.title)

        # redirect to the books directory
        return redirect(url_for('directory.list_books'))

    # form.description.data = department.description
    # form.name.data = department.name
    return render_template('directory/book.html', action="Edit",
                           add_book=add_book, form=form,
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

#edit book
    #add description
#delete book