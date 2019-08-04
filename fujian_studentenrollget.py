#FUJIAN Discovery tool for SUT REG
#!Python

import re
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

info = []

def fetchall(studentid):
    require_page = 'https://reg.sut.ac.th/registrar/learn_time.asp?studentid=1' + studentid + '&f_cmd=2'
    return require_page

def urlreturn(stdid):
    require_page = 'https://reg.sut.ac.th/registrar/learn_time.asp?studentid=1' + stdid + '&f_cmd=2'
    return require_page

def getstudent_name(stdid):
    r = requests.post("https://reg.sut.ac.th/registrar/learn_time.asp", data=dict(
        f_cmd="1",
        f_studentcode=stdid,
        f_studentname="",
        f_studentsurname="",
        f_studentstatus="all",
        departmentid="",
        programid="",
        f_maxrows="25"
    ))
    r.encoding = r.apparent_encoding
    sr = BeautifulSoup(r.text, 'html.parser')

    namet = []
    for mmp in sr.find_all('font', attrs={'face': 'MS Sans Serif', 'size': '3'}):
        namet.append(mmp.find("font").text)

    try:
        mrx = re.sub('<.*?>', '', str(namet[0])).replace('\xa0', '')
        xm = mrx.strip("[]")
    except IndexError:
        xm = "Error To Get"

    return xm

def getstudentenrollment(url):
    page = urlopen(url)
    webpage = BeautifulSoup(page, 'html.parser')
    web = webpage.find_all('font', attrs={'face': 'MS Sans Serif', 'size': '3'})

    lengthweb = len(web)
    subject = []

    for v in range(lengthweb):
        subject.append(web[v])

    cleaner = sanitizehtml(subject,lengthweb)

    return cleaner

def getstudentenrollment_raw(url):
    page = urlopen(url)
    webpage = BeautifulSoup(page, 'html.parser')
    web = webpage.find_all('font', attrs={'face': 'MS Sans Serif', 'size': '3'})

    lengthweb = len(web)
    subject = []

    for v in range(lengthweb):
        subject.append(web[v])

    return subject

def getinstitute(content):
    institute = content[5]
    return re.sub('<.*?>', '', str(institute)).replace('\xa0', '')


def getminor(content):
    minor = content[7]
    return re.sub('<.*?>', '', str(minor)).replace('\xa0', '')

def getassistant(content):
    assistant = content[9]
    return re.sub('<.*?>', '', str(assistant)).replace('\xa0', '')

def sanitizehtml(content,lengthweb):
    countenroll = 0
    fullcontent = []
    temp = ""
    sanitizer = ""

    for v in range(11, lengthweb):
        if v % 2 == 0:
            countenroll = countenroll + 1
        temp = content[v]
        sanitizer = re.sub('<.*?>', '', str(temp)).replace('\xa0', '')
        fullcontent.append(sanitizer)

    return fullcontent


def getsanit_subject_without_groupnum(fullcontent):
    vx = 0
    withoutgroupnum = []
    i = 0
    for respond in fullcontent:
        if i % 2 == 0:
            withoutgroupnum.append(respond)
        else:
            vx = vx + 1
        i = i + 1

    return withoutgroupnum
