# ucbschedule

Code for scraping data from the UC Berkeley Schedule of Classes and
analyzing it.

## Requirements

The project requires Python 2.6 or 2.7 (untested with other versions),
as well as several Python packages, including BeautifulSoup, Requests,
and Flask.

## Scraping

Use `runscraper.py` to run the scrapers. There are two:

* Department scraper (`dept_scraper.py`): Scrapes department names and
  abbreviations from ScheduleBuilder.
* Section scraper (`section_scraper.py`): Scrapes all info from the
  [UCB Schedule of Classes](http://schedule.berkeley.edu) for today.

## Web Application

`ucbschedule.py` is a Flask application that provides an API and views
for the statistics of the data set. The API is provided using
Flask-Restless. 

## Statistics

Currently, the following information is extracted:

* Which classes have the most enrolled or waitlisted students as a
  percentage of their seat limit
* Which classes have the highest seat limit
* Which rooms are used the most
