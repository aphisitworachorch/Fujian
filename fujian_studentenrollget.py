#FUJIAN Discovery tool for SUT REG
#!Python

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

info = []

def fetchall(studentid):
    require_page = 'http://reg5.sut.ac.th/registrar/learn_time.asp?studentid=1' + studentid + '&f_cmd=2'
    return require_page

def urlreturn(stdid):
    require_page = 'http://reg5.sut.ac.th/registrar/learn_time.asp?studentid=1' + stdid + '&f_cmd=2'
    return require_page

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
    withoutgroupnum = []
    i = 0
    for respond in fullcontent:
        if i % 2 == 0:
            withoutgroupnum.append(respond)
        else:
            print()
        i = i + 1

    return withoutgroupnum