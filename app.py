from flask import Flask, render_template, json, request, session, redirect
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import os

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'shh its a secret!!!!?'

# MySQL configurations

#attempt at grabbing env vars
#app.config['MYSQL_DATABASE_USER'] = os.environ['DB_USER']
#app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['DB_PASS']
#app.config['MYSQL_DATABASE_DB'] = os.environ['DB_NAME']
#app.config['MYSQL_DATABASE_HOST'] = os.environ['CLEARDB_DATABASE_URL']
#app.config['MYSQL_DATABASE_HOST'] = os.environ['DB_HOST']
#mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/Services')
def Services():
    return render_template('services.html')

@app.route('/About')
def About():
    return render_template('about.html')

@app.route('/error404')
def error404():
    return render_template('404.html')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
