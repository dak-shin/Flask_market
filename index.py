
# TODO: set FLASK_APP=nameofthefile.py
# TODO: set FLASK_ENV=development
# FLASK RUN

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def helloThere():
    return render_template('home.html')


@app.route('/<user>')
def helloworld(user):
    return f"<h1>Hello there {user}</h1>"
