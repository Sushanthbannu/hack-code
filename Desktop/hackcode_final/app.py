from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user

from models import db, User
from auth import auth
from admin import admin_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(admin_bp)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/books')
def books():
    return render_template('books.html')

@app.route('/book-viewer')
def book_viewer():
    return render_template('book-viewer.html')

@app.route('/courses/<course_name>')
def course_page(course_name):
    try:
        return render_template(f'courses/{course_name}.html')
    except:
        return "Course not found", 404

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('auth/dashboard.html', name=current_user.name)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
