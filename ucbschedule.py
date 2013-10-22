from flask import Flask, render_template
from flask.ext.restless import APIManager
from sqlalchemy.orm import scoped_session
from scraper import Session
from scraper.models import Department, Course, Section, SectionInstance
from scraper.stats import most_full_filters

app = Flask(__name__)

# initialize API
session = scoped_session(Session)
manager = APIManager(app, session=session)
manager.create_api(Department)
manager.create_api(Course)
manager.create_api(Section)
manager.create_api(SectionInstance)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mostfull')
def mostfull():
    full = most_full_filters(session)
    return render_template('mostfull.html', full=full)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()
