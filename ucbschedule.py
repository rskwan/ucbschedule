from datetime import date
from decimal import Decimal, ROUND_DOWN
from flask import Flask, request, render_template
from flask.ext.restless import APIManager
from sqlalchemy.orm import scoped_session
from schedule import Session
from schedule.models import Department, Course, Section, SectionInstance
from schedule.stats import most_full_filters, biggest_filters

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

@app.route('/mostfull/', methods=['GET', 'POST'])
def mostfull():
    error = None
    if request.method == 'POST':
        try:
            year = int(request.form['year'])
            month = int(request.form['month'])
            day = int(request.form['day'])
            d = date(year, month, day)
        except:
            d = date.today()
        try:
            if request.form['dept'] != 'all':
                dept = session.query(Department).\
                               filter(Department.abbreviation == request.form['dept']).\
                               first()
            else:
                dept = None
        except:
            dept = None
        full = most_full_filters(session, day=d, dept=dept, fmt='LEC')
    else:
        full = most_full_filters(session, fmt='LEC')
    depts = session.query(Department.abbreviation, Department.name).all()
    if full:
        ranked = []
        for i in range(len(full)):
            pair = full[i]
            percent = Decimal(str(pair[1])).quantize(Decimal('.01'),
                                                     rounding=ROUND_DOWN)
            if i > 0 and percent == ranked[i - 1][2]:
                rank = ranked[i - 1][0]
            else:
                rank = i + 1
            triplet = (rank, pair[0], percent)
            ranked.append(triplet)
    else:
        ranked = None
    return render_template('mostfull.html', ranked=ranked, depts=depts)

@app.route('/biggest/', methods=['GET', 'POST'])
def biggest():
    error = None
    if request.method == 'POST':
        try:
            if request.form['dept'] != 'all':
                dept = session.query(Department).\
                               filter(Department.abbreviation == request.form['dept']).\
                               first()
            else:
                dept = None
        except:
            dept = None
        big = biggest_filters(session, dept=dept)
    else:
        big = biggest_filters(session)
    depts = session.query(Department.abbreviation, Department.name).all()
    ranked = []
    for i in range(len(big)):
        pair = big[i]
        if i > 0 and pair[1] == ranked[i - 1][2]:
            rank = ranked[i - 1][0]
        else:
            rank = i + 1
        triplet = (rank, pair[0], pair[1])
        ranked.append(triplet)
    return render_template('biggest.html', ranked=ranked, depts=depts)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()
