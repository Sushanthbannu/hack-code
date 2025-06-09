from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Course, Book

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

def admin_only(func):
    from functools import wraps
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return "Access denied", 403
        return func(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_only
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/courses', methods=['GET', 'POST'])
@login_required
@admin_only
def manage_courses():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        filename = request.form['filename']
        course = Course(title=title, description=description, filename=filename)
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully.')
    courses = Course.query.all()
    return render_template('admin/courses.html', courses=courses)

@admin_bp.route('/books', methods=['GET', 'POST'])
@login_required
@admin_only
def manage_books():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        thumbnail = request.form.get('thumbnail', '')
        book = Book(title=title, url=url, thumbnail=thumbnail)
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully.')
    books = Book.query.all()
    return render_template('admin/books.html', books=books)
