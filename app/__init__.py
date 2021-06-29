import os
from flask import Flask, render_template, send_from_directory, request
from dotenv import load_dotenv
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db


load_dotenv()
app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.getcwd(), 'flask.sqlite')
db.init_app(app)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/about/ishika')
def about_ishika():
    return render_template('ishika.html', fellowName='Ishika');

@app.route('/about/frankie')
def about_frankie():
    return render_template('frankie.html', fellowName='Frankie');

@app.route('/about/sebastian')
def about_sebastian():
    return render_template('sebastian.html', fellowName='Sebastian');
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/post')
def post():
    return render_template('post.html', title="Post")

# Logic for /health, deploting to EC2
@app.route('/health', methods=['GET'])
def health():
    return render_template('health.html')

# Register route logic
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return f"User {username} created successfully"
        else:
            return error, 418

    ## TODO: Return a restister page
    return render_template('register.html')

#Login logic

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            return "Login Successful", 200 
        else:
            return error, 418
    
    ## TODO: Return a login page
    return render_template('login.html')