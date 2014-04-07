from datetime import date, datetime
from sqlalchemy.sql import func
from .models import Department, Course, Section, SectionInstance

def most_full(n, instances):
    """Returns the N (int) most full sections out of INSTANCES."""
    pairs = []
    for instance in instances:
        fullness = (100.0 * (instance.enrolled + instance.waitlist)) \
                   / instance.limit
        pairs.append((instance, fullness))
    pairs.sort(key=lambda x: x[1])
    pairs.reverse()
    results = []
    cutoff = pairs[:n][-1][1]
    for pair in pairs:
        if pair[1] >= cutoff:
            results.append(pair)
        else:
            break
    return results

def most_full_filters(session, day=date.today(), dept=None, fmt=None, n=30):
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

def biggest(n, instances):
    """Returns the N (int) biggest (i.e. with highest seat limit) sections
    out of INSTANCES."""
    pairs = []
    for instance in instances:
        pairs.append((instance, instance.limit))
    pairs.sort(key=lambda x: x[1])
    pairs.reverse()
    results = []
    cutoff = pairs[:n][-1][1]
    for pair in pairs:
        if pair[1] >= cutoff:
            results.append(pair)
        else:
            break
    return results

def biggest_filters(session, day=date.today(), dept=None, n=30):
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
    if instances.count() > 0:
        return biggest(n, instances.all())
    else:
        return None

def print_biggest(big):
    if big:
        print "Biggest classes:"
        for pair in big:
            print "{0}: {1} seats".format(pair[0], pair[1])
    else:
        print "No sections given."

def popular_rooms(session, day=date.today(), fmt=None, n=25):
    query = session.query(SectionInstance.location, func.count('*')).\
                    filter(SectionInstance.location != '').\
                    group_by(SectionInstance.location)
    if fmt:
        fmt_section_ids = session.query(Section.id).\
                                  filter(Section.section_format == fmt).\
                                  subquery()
        query = query.filter(SectionInstance.section_id.in_(fmt_section_ids))
    pairs = query.all()
    pairs.sort(key=lambda p: p[1])
    pairs.reverse()
    results = []
    cutoff = pairs[:n][-1][1]
    for pair in pairs:
        if pair[1] >= cutoff:
            results.append(pair[0])
        else:
            break
    return results

def print_popular_rooms(rooms):
    if rooms:
        print "Most popular rooms:"
        for pair in rooms:
            print "{0}: {1} sections".format(pair[0], pair[1])
    else:
        print "No rooms given."
