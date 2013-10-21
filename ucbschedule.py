from flask import Flask
from flask.ext.restless import APIManager
from sqlalchemy.orm import scoped_session
from scraper import Session
from scraper.models import Department, Course, Section

app = Flask(__name__)

# initialize API
session = scoped_session(Session)
manager = APIManager(app, session=session)
manager.create_api(Department)
manager.create_api(Course)
manager.create_api(Section)

@app.route('/')
def index():
    return "Access the API at /api/."

if __name__ == '__main__':
    app.run()
