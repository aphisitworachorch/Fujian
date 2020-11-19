from flask import Flask, render_template

from webdriver import fujian
from flask import jsonify
from flask_caching import Cache

import datetime
import redis

app = Flask(__name__)
r = redis.Redis(host=redis)

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'fujian_',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': '6379'})


@app.route('/')
def hello_world():
    return 'Fujian SD2E'


@app.route('/student/<student_id>', methods=['POST'])
def getStudentEnroll(student_id):
    yearofstudent = str(student_id)[1:3]
    student_name = fujian.getstudent_name(student_id)
    student_id = student_id
    prefix = str(fujian.identifyStudentID(student_id)["number"])
    degree = str(fujian.identifyStudentID(student_id)["degree"])
    fetchstudent_info = fujian.fetchall(prefix + "" + str(student_id)[1:10])
    subject_id = fujian.getstudentenrollment_id(fetchstudent_info)
    raw_student = fujian.getstudentenrollment_raw(fetchstudent_info)
    subject = fujian.getsanit_subject_without_groupnum(subject_id)
    subject_name = fujian.getstudentenrollment_name(fetchstudent_info)
    institute = fujian.getinstitute(raw_student)
    minor = fujian.getminor(raw_student)
    assistant = fujian.getassistant(raw_student)

    calculate = 0
    now = datetime.datetime.now()
    if (int(now.year + 543) % 100) - (int(yearofstudent)) <= 0:
        calculate = 1
    else:
        calculate = (int(now.year + 543) % 100) - (int(yearofstudent))

    data = {
        "student_id": student_id,
        "student_name": student_name,
        "institute": institute,
        "minor": minor,
        "assistant": assistant,
        "enroll_subjects": subject_id,
        "enroll_subjects_name": subject_name,
        "year_of_student": calculate
    }

    redis_data = cache.get(student_id)
    if redis_data is None:
        cache.set(student_id, data)
        return jsonify(data)
    else:
        return jsonify(redis_data)


@app.route('/student/<student_id>/<eduyear>', methods=['POST'])
def getStudentEnroll_EDUYEAR(student_id, eduyear):
    yearofstudent = str(student_id)[1:3]
    student_name = fujian.getstudent_name(student_id)
    student_id = student_id
    prefix = str(fujian.identifyStudentID(student_id)["number"])
    degree = str(fujian.identifyStudentID(student_id)["degree"])
    fetchstudent_info = fujian.fetchall_eduyear(prefix + "" + str(student_id)[1:10], str(eduyear))
    subject_id = fujian.getstudentenrollment_id(fetchstudent_info)
    raw_student = fujian.getstudentenrollment_raw(fetchstudent_info)
    subject = fujian.getsanit_subject_without_groupnum(subject_id)
    subject_name = fujian.getstudentenrollment_name(fetchstudent_info)
    institute = fujian.getinstitute(raw_student)
    minor = fujian.getminor(raw_student)
    assistant = fujian.getassistant(raw_student)

    calculate = 0
    now = datetime.datetime.now()
    if (int(now.year + 543) % 100) - (int(yearofstudent)) <= 0:
        calculate = 1
    else:
        calculate = (int(now.year + 543) % 100) - (int(yearofstudent))

    data = {
        "eduyear": eduyear,
        "student_id": student_id,
        "student_name": student_name,
        "institute": institute,
        "minor": minor,
        "assistant": assistant,
        "enroll_subjects": subject_id,
        "enroll_subjects_name": subject_name,
        "year_of_student": calculate
    }

    redis_data = cache.get(student_id+'_eduyear_'+eduyear)
    if redis_data is None:
        cache.set(student_id+'_eduyear_'+eduyear, data)
        return jsonify(data)
    else:
        return jsonify(redis_data)


@app.route('/student/<student_id>/<eduyear>/<term>', methods=['POST'])
def getStudentEnroll_EDUYEAR_TERM(student_id, eduyear, term):
    yearofstudent = str(student_id)[1:3]
    student_name = fujian.getstudent_name(student_id)
    student_id = student_id
    prefix = str(fujian.identifyStudentID(student_id)["number"])
    degree = str(fujian.identifyStudentID(student_id)["degree"])
    fetchstudent_info = fujian.fetchall_eduyear_term(prefix + "" + str(student_id)[1:10], str(eduyear), str(term))
    subject_id = fujian.getstudentenrollment_id(fetchstudent_info)
    raw_student = fujian.getstudentenrollment_raw(fetchstudent_info)
    subject = fujian.getsanit_subject_without_groupnum(subject_id)
    subject_name = fujian.getstudentenrollment_name(fetchstudent_info)
    institute = fujian.getinstitute(raw_student)
    minor = fujian.getminor(raw_student)
    assistant = fujian.getassistant(raw_student)

    calculate = 0
    now = datetime.datetime.now()
    if (int(now.year + 543) % 100) - (int(yearofstudent)) <= 0:
        calculate = 1
    else:
        calculate = (int(now.year + 543) % 100) - (int(yearofstudent))

    data = {
        "eduyear": eduyear,
        "term": term,
        "student_id": student_id,
        "student_name": student_name,
        "institute": institute,
        "minor": minor,
        "assistant": assistant,
        "enroll_subjects": subject_id,
        "enroll_subjects_name": subject_name,
        "year_of_student": calculate
    }

    redis_data = cache.get(student_id+'_eduyear_'+eduyear+'_term_'+term)
    if redis_data is None:
        cache.set(student_id+'_eduyear_'+eduyear+'_term_'+term, data)
        return jsonify(data)
    else:
        return jsonify(redis_data)


@app.route('/student/<student_id>', methods=['GET'])
@cache.cached(timeout=50, key_prefix='page_<student_id>')
def getStudentHTML(student_id):
    yearofstudent = str(student_id)[1:3]
    student_name = fujian.getstudent_name(student_id)
    student_id = student_id
    prefix = str(fujian.identifyStudentID(student_id)["number"])
    degree = str(fujian.identifyStudentID(student_id)["degree"])
    fetchstudent_info = fujian.fetchall(prefix + "" + str(student_id)[1:10])
    subject_id = fujian.getstudentenrollment_id(fetchstudent_info)
    raw_student = fujian.getstudentenrollment_raw(fetchstudent_info)
    subject = fujian.getsanit_subject_without_groupnum(subject_id)
    subject_name = fujian.getstudentenrollment_name(fetchstudent_info)
    institute = fujian.getinstitute(raw_student)
    minor = fujian.getminor(raw_student)
    assistant = fujian.getassistant(raw_student)

    calculate = 0
    now = datetime.datetime.now()
    if (int(now.year + 543) % 100) - (int(yearofstudent)) <= 0:
        calculate = 1
    else:
        calculate = (int(now.year + 543) % 100) - (int(yearofstudent))

    return render_template('student.html',
                           degree=degree,
                           yr=calculate,
                           lensub=len(subject_id),
                           subject_id=subject_id,
                           subject_name=subject_name,
                           student_name=student_name,
                           student_id=student_id,
                           institute=institute,
                           minor=minor,
                           assistant=assistant)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
