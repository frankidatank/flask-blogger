import os
from flask import Flask, render_template, send_from_directory, request
from dotenv import load_dotenv
from . import db

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
