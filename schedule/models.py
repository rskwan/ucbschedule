from datetime import date
from sqlalchemy import Column, Sequence, ForeignKey, Integer, String, Text, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from . import engine

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, Sequence('dept_id_seq'), primary_key=True)
    name = Column(String(50))
    abbreviation = Column(String(10))

    def __repr__(self):
        return "<Department: {0} ({1})>".format(self.name,
                                                self.abbreviation)

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, Sequence('course_id_seq'), primary_key=True)
    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship("Department", backref=backref('courses', order_by=id))
    number = Column(String(10))
    semester = Column(String(10))
    year = Column(Integer)

    def __repr__(self):
        return "<Course: {0} {1} ({2} {3})>".format(self.department.abbreviation,
                                                    self.number,
                                                    self.semester,
                                                    self.year)


class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, Sequence('section_id_seq'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship("Course", backref=backref('sections', order_by=id))
    section_format = Column(String(5))
    section_number = Column(String(5))

    def __str__(self):
        return "{0} {1} {2} {3} ({4} {5})".format(self.course.department.abbreviation,
                                                  self.course.number,
                                                  self.section_format,
                                                  self.section_number,
                                                  self.course.semester,
                                                  self.course.year)

class SectionInstance(Base):
    __tablename__ = 'section_instances'

    id = Column(Integer, Sequence('section_instance_id_seq'), primary_key=True)
    section_id = Column(Integer, ForeignKey('sections.id'))
    section = relationship("Section", backref=backref('instances', order_by=id))
    location = Column(String(50))
    days = Column(String(10))
    time = Column(String(10))
    instructor = Column(String(50))
    status = Column(String(50))
    ccn = Column(String(50))
    units = Column(String(50))
    # session_dates, summer_fees: only summer classes
    session_dates = Column(String(50))
    summer_fees = Column(String(50))
    # final_exam_group, restrictions: only fall/spring classes
    final_exam_group = Column(String(50))
    restrictions = Column(String(50))
    note = Column(Text)
    enrolled = Column(Integer)
    limit = Column(Integer)
    waitlist = Column(Integer)
    update_date = Column(Date)

    def __init__(self, section_id, section, location, days, time, instructor, status,
                 ccn, units, session_dates, summer_fees, final_exam_group, restrictions,
                 note, enrolled, limit, waitlist, update_date=date.today()):
        self.section_id = section_id
        self.section = section
        self.location = location
        self.days = days
        self.time = time
        self.instructor = instructor
        self.status = status
        self.ccn = ccn
        self.units = units
        self.session_dates = session_dates
        self.summer_fees = summer_fees
        self.final_exam_group = final_exam_group
        self.restrictions = restrictions
        self.note = note
        self.enrolled = enrolled
        self.limit = limit
        self.waitlist = waitlist
        self.update_date = update_date

    def __str__(self):
        return str(self.section) + " ({0})".format(self.update_date)

Base.metadata.create_all(engine)
