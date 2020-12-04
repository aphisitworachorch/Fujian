import os
import random

from flask import Flask, render_template, json
from flask_selfdoc import Autodoc
from werkzeug.exceptions import HTTPException

from webdriver import fujian
from flask import jsonify
from flask_caching import Cache

import datetime
import redis

app = Flask(__name__)
auto = Autodoc(app)
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
@auto.doc()
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
@auto.doc()
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

    redis_data = cache.get(student_id + '_eduyear_' + eduyear)
    if redis_data is None:
        cache.set(student_id + '_eduyear_' + eduyear, data)
        return jsonify(data)
    else:
        return jsonify(redis_data)


@app.route('/student/<student_id>/<eduyear>/<term>', methods=['POST'])
@auto.doc()
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

    redis_data = cache.get(student_id + '_eduyear_' + eduyear + '_term_' + term)
    if redis_data is None:
        cache.set(student_id + '_eduyear_' + eduyear + '_term_' + term, data)
        return jsonify(data)
    else:
        return jsonify(redis_data)


@app.route('/student/<student_id>', methods=['GET'])
@cache.cached(timeout=(60 * 5))
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

    images_file = []
    for filename in os.listdir('static/img/tech'):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            images_file.append(os.path.join('img/tech', filename))
        else:
            continue
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
                           assistant=assistant, images_file=images_file)


@app.errorhandler(HTTPException)
def handle_exception(e):
    error_link = ['https://www.youtube.com/embed/7Hvkhh4GaI0?controls=0&autoplay=1',
                  'https://www.youtube.com/embed/PFygXz-Y0zA?controls=0&autoplay=1',
                  'https://www.youtube.com/embed/wpHlagmXzxY?controls=0&autoplay=1',
                  'https://www.youtube.com/embed/v5aepf1t5CU?controls=0&autoplay=1',
                  'https://www.youtube.com/embed/u06GqlNiJUY?controls=0&autoplay=1',
                  'https://www.youtube.com/embed/ztxs6nixsaI?controls=0&autoplay=1',
                  'https://www.youtube.com/embed/1iqd-AL6soE?controls=0&autoplay=1',
                  'https://www.youtube.com/embed/-OAPdG8sgLs?controls=0&autoplay=1&start=166',
                  'https://www.youtube.com/embed/0GFKs17cjWs?controls=0&autoplay=1',
                  'https://www.youtube.com/embed/pAP9qcjPvtE?controls=0&autoplay=1',
                  'https://www.youtube.com/embed/k2CXu4K40bg?controls=0&autoplay=1',
                  'https://www.youtube.com/embed/hmj-RT3S-d4?controls=0&autoplay=1&start=5',
                  'https://www.youtube.com/embed/0QYGWXEXZwU?controls=0&autoplay=1']
    # error_link = ['https://www.youtube.com/embed/uefcQzHmA_Y?controls=0&autoplay=1']
    rd = random.randint(0, len(error_link) - 1)
    error_random = random.randint(100, 600)
    return render_template('error.html', error_link=error_link[rd], log=e, error_code=error_random), int(error_random)


@app.route('/documentation')
def documentation():
    return auto.html()


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
