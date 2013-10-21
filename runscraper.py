from scraper import dept_scraper, section_scraper

# get department data from ScheduleBuilder
dept_scraper.run()

# get section info
section_scraper.run('Spring', 2014)
