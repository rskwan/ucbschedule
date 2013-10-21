from sqlalchemy import Column, Sequence, ForeignKey, Integer, String, Text, DateTime
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
    title = Column(String(50))
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
    section_format = Column(String(5))
    section_number = Column(String(5))
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
    final_exam_group = Column(String(5))
    restrictions = Column(String(50))
    note = Column(Text)
    enrolled = Column(Integer)
    limit = Column(Integer)
    waitlist = Column(Integer)
    update_datetime = Column(DateTime)

Base.metadata.create_all(engine)