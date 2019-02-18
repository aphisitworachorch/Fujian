import fujian_studentenrollget as fj
import csv

v = 0
studentid = ['','']
file = open('datafor_student.csv','w', encoding='utf-8-sig')
write = csv.writer(file, delimiter=',')

with open("student_feb19.csv", encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        finalstd = str(row).replace('\ufeff','')
        for i in range(0,len(row)):
            # Start to Scraping Web
            studentget = fj.fetchall(str(finalstd)[3:10])
            print(studentget)
            # Start to bringing out a Subject as Array
            subject = fj.getstudentenrollment(studentget)
            sanitizesubject = fj.getsanit_subject_without_groupnum(subject)
            # Raw Raw Raw Raw and Raw
            raw = fj.getstudentenrollment_raw(studentget)

            # Institute / Minor / Assistant that you want it !
            institute = fj.getinstitute(raw)
            minor = fj.getminor(raw)
            asst = fj.getassistant(raw)

            # Print Out ! <3
            # print(subject)
            write.writerow((str(finalstd)[2:10], institute, minor, asst, ",".join(sanitizesubject)))
            print("Get information from -> ", str(finalstd)[2:10], " <- Completed ! ")
            print("")

file.close()
print(i)