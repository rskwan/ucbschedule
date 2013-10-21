import argparse
from scraper import dept_scraper, section_scraper

VALID_SEMESTERS = [('Spring', 2014)]

parser = argparse.ArgumentParser(description="Scrape the UCB Schedule of Classes.")
parser.add_argument('type', type=str, help="type of scraping (department or section).")
parser.add_argument('--semester', help="semester (Fall, Spring, or Summer)")
parser.add_argument('--year', help='year (integer)')

args = parser.parse_args()
print "type: {0}, semester: {1}, year: {2}".format(args.type,
                                                   args.semester,
                                                   args.year)

if args.type == 'department':
    dept_scraper.run()

if args.type == 'section':
    semester = args.semester
    year = args.year
    try:
        year = int(year)
    except:
        raise ValueError("Invalid year.")
    if (semester, year) not in VALID_SEMESTERS:
        raise ValueError("Invalid semester/year.")
    section_scraper.run(semester, year)

