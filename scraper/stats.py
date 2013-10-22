from datetime import date
from . import Session
from .models import Department, Course, Section, SectionInstance

def most_full(n, instances):
    """Returns the N (int) most full sections out of INSTANCES."""
    pairs = []
    for instance in instances:
        fullness = (100.0 * (instance.enrolled + instance.waitlist)) \
                   / instance.limit
        pairs.append((str(instance.section), fullness))
    pairs.sort(key=lambda x: x[1])
    pairs.reverse()
    return pairs[:n]

def most_full_filters(session, day=date.today(), dept=None, fmt=None, n=25):
    instances = session.query(SectionInstance).\
                        filter(SectionInstance.update_date == day).\
                        filter(SectionInstance.limit != 0)
    if dept:
        dept_course_ids = session.query(Course.id).\
                                  filter(Course.department_id == dept.id).\
                                  subquery()
        dept_section_ids = session.query(Section.id).\
                                   filter(Section.course_id.in_(dept_course_ids)).\
                                   subquery()
        instances = instances.filter(SectionInstance.section_id.in_(dept_section_ids))
    if fmt:
        fmt_section_ids = session.query(Section.id).\
                                  filter(Section.section_format == fmt).\
                                  subquery()
        instances = instances.filter(SectionInstance.section_id.in_(fmt_section_ids))
    if instances.count() > 0:
        return most_full(n, instances.all())
    else:
        return None

def print_most_full(full):
    if full:
        print "Most full sections:"
        for pair in full:
            print "%s: %.2f percent full" % pair
    else:
        print "No sections given."
