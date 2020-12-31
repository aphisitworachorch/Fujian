import random

from webdriver import fujian
from webdriver.brisbane import Brisbane
import datetime


class FujianCore:
    def __init__(self, student_id, term=None, eduyear=None):
        self.name = 'Fujian v3X'
        self.student_id = student_id
        self.brisbane_term = 2
        self.brisbane_eduyear = 2563
        self.header = None
        self.prefix = str(fujian.identifyStudentID(self.student_id)["number"])
        self.degree = str(fujian.identifyStudentID(self.student_id)["degree"])
        self.preformat_student_id = self.prefix + "" + str(self.student_id)[1:10]
        self.gzr = [eduyear, term]
        if eduyear is not None:
            self.fetchstudent_info = fujian.fetchall_eduyear(self.preformat_student_id, eduyear)
        if eduyear is not None and term is not None:
            self.fetchstudent_info = fujian.fetchall_eduyear_term(self.preformat_student_id, eduyear, term)
        if term and eduyear is None:
            self.fetchstudent_info = fujian.fetchall(self.preformat_student_id)

    def obfuscate(self, object_name):
        object_length = len(object_name)
        return ''.join(
            map(str, random.choices(object_name, k=random.randint(2, object_length)))) + ' [OBFUSCATED FOR PRIVACY]'

    def getStudentInfo(self):
        yearofstudent = str(self.student_id)[1:3]
        hidden_name = fujian.getstudent_name(self.student_id)
        student_name = self.obfuscate(hidden_name)
        subject_id = fujian.getstudentenrollment_id(self.fetchstudent_info)
        raw_student = fujian.getstudentenrollment_raw(self.fetchstudent_info)
        subject = fujian.getsanit_subject_without_groupnum(subject_id)
        subject_name = fujian.getstudentenrollment_name(self.fetchstudent_info)
        institute = fujian.getinstitute(raw_student)
        minor = fujian.getminor(raw_student)
        hidden_assistant = fujian.getassistant(raw_student)
        assistant = self.obfuscate(hidden_assistant)

        now = datetime.datetime.now()
        if (int(now.year + 543) % 100) - (int(yearofstudent)) <= 0:
            calculate = 1
        else:
            calculate = (int(now.year + 543) % 100) - (int(yearofstudent))

        data = {
            "student_id": self.student_id,
            "student_name": student_name,
            "institute": institute,
            "minor": minor,
            "assistant": assistant,
            "enroll_subjects": subject_id,
            "enroll_subjects_name": subject_name,
            "year_of_student": calculate,
            "degree": self.degree,
            "graduated_for": calculate
        }

        return data
