import re
import requests
from bs4 import BeautifulSoup
from tidylib import tidy_document
from . import engine, Session
from .models import Department, Course, Section 

SEMESTERS = { 'Fall': 'FL', 'Spring': 'SP', 'Summer': 'SU' }

def scrape_sections(semester, year, session):
    for dept in session.query(Department).order_by(Department.abbreviation):
        search_dept(dept, semester, year, session)

def search_dept(dept, semester, year, session):
    payload = { 'p_term': SEMESTERS[semester],
                'p_deptname': '-- Choose a Department Name --',
                'p_classif': '-- Choose a Course Classification --',
                'p_presuf': '-- Choose a Course Prefix/Suffix --',
                'p_dept': dept.abbreviation }
    r = requests.post('http://osoc.berkeley.edu/OSOC/osoc', params=payload)
    txt, err = tidy_document(r.text)
    analyze_html(txt, dept, semester, year, session)

    # get the total rows so we can keep searching
    soup = BeautifulSoup(txt)
    tables = soup.find_all('table')
    a = tables[0].find_all('tr')[1].find_all('td')[1].a
    if a:
        # use regex to get the total rows out of the 'see next results' link
        match = re.search('p_total_rows=\d+', str(a['href']))
        if match:
            totalrows = int(match.group().split('=')[1])
            # each page displays 100 rows (sections); index starts with 1, not 0
            for i in range(1, ((totalrows/100)+1)):
                payload['p_start_row'] = str(100*i + 1)
                r = requests.post('http://osoc.berkeley.edu/OSOC/osoc',
                                  params=payload)
                txt, err = tidy_document(r.text)
                analyze_html(txt, semester, year, session)

def analyze_html(txt, dept, semester, year, session):
    soup = BeautifulSoup(txt)

    # each section is displayed as a table
    tables = soup.find_all('table')
    sections = tables[1:(len(tables)-1)]

    for section in sections:
        analyze_section(section, dept, semester, year, session)

def analyze_section(section, dept, semester, year, session):
    rows = section.find_all('tr')
    inputs = section.find_all('input')

    # split 'STATISTICS 2 P 001 LEC' into ['STATISTICS', '2', 'P', '001', 'LEC']
    section_info = rows[0].find_all('td')[2].b.string.strip()
    print section_info
    section_info_parts = section_info.split()
    course_number = section_info_parts[-4].strip()
    section_number = section_info_parts[-2].strip()
    section_format = section_info_parts[-1].strip()

    # usually in the format 'TuTh 5-6:30P, 155 DWINELLE'
    timeplace = rows[2].find_all('td')[1].tt.string.strip().split(', ')
    if len(timeplace) > 1:
        # normal course
        days = timeplace[0].split()[0]
        time = timeplace[0].split()[1]
        location = timeplace[1]
    else:
        # special case
        days = time = location = ''

    instructor = blank_if_none(rows[3].find_all('td')[1].tt)
    status = blank_if_none(rows[4].find_all('td')[1].tt)
    ccn = blank_if_none(rows[5].find_all('td')[1].tt)
    units = blank_if_none(rows[6].find_all('td')[1].tt)

    if semester != 'Summer':
        final_exam_group = blank_if_none(rows[7].find_all('td')[1].tt)
        restrictions = blank_if_none(rows[8].find_all('td')[1].tt)
        session_dates = summer_fees = ''
    else:
        final_exam_group = restrictions = ''
        session_dates = blank_if_none(rows[7].find_all('td')[1].tt)
        summer_fees = blank_if_none(rows[8].find_all('td')[1].tt)

    note = blank_if_none(rows[9].find_all('td')[1].tt)

    enrollnums = rows[10].find_all('td')[1].tt.string.strip().split()[:3]
    try:
        limit = int(enrollnums[0][6:])
        enrolled = int(enrollnums[1][9:])
        waitlist = int(enrollnums[2][9:])
    except:
        limit = enrolled = waitlist = 0

    c = get_course(dept, course_number, semester, year, session)
    if c is None:
        c = Course(department_id=dept.id, department=dept, number=course_number,
                   semester=semester, year=year)
        session.add(c)

    s = Section(c.id, c, section_format, section_number, location, days, time,
                instructor, status, ccn, units, session_dates, summer_fees,
                final_exam_group, restrictions, note, enrolled, limit, waitlist)
    session.add(s)

def get_course(dept, number, semester, year, session):
    query = session.query(Course).filter_by(department=dept, number=number,
                                            semester=semester, year=year)
    if query.count() > 0:
        return query.first()
    else:
        return None

def blank_if_none(tt):
    if tt:
        return tt.text.strip()
    else:
        return ''

def run(semester, year):
    session = Session()
    try:
        scrape_sections(semester, year, session)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close() 
