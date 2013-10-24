from datetime import date
from decimal import Decimal, ROUND_DOWN
from flask import Flask, render_template
from flask.ext.restless import APIManager
from sqlalchemy.orm import scoped_session
from scraper import Session
from scraper.models import Department, Course, Section, SectionInstance
from scraper.stats import most_full_filters, biggest_filters

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

@app.route('/mostfull/')
def mostfull():
    full = most_full_filters(session, fmt='LEC')
    ranked = []
    for i in range(len(full)):
        pair = full[i]
        percent = Decimal(pair[1]).quantize(Decimal('.01'),
                                            rounding=ROUND_DOWN)
        if i > 0 and percent == ranked[i - 1][2]:
            rank = ranked[i - 1][0]
        else:
            rank = i + 1
        triplet = (rank, pair[0], percent)
        ranked.append(triplet)
    return render_template('mostfull.html', ranked=ranked)

@app.route('/biggest/')
def biggest():
    big = biggest_filters(session)
    ranked = []
    for i in range(len(big)):
        pair = big[i]
        if i > 0 and pair[1] == ranked[i - 1][2]:
            rank = ranked[i - 1][0]
        else:
            rank = i + 1
        triplet = (rank, pair[0], pair[1])
        ranked.append(triplet)
    return render_template('biggest.html', ranked=ranked)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()
