# download_exams
# Interactive exam downloader for Tufts' webcenter.

# Hack around so we can import webcenter.
import os, sys
lib_path = os.path.abspath('../webcenter/')
sys.path.append(lib_path)

from webcenter import *
try:
    from webcenter_credentials import *
except:
    STUDENT_ID = None
    SIS_PIN = None

if not STUDENT_ID or not SIS_PIN:
    STUDENT_ID = raw_input("Please enter your student ID: ")
    SIS_PIN = raw_input("Please enter your SIS pin: ")

# Initiate a session.
wc = WebcenterSession(STUDENT_ID, SIS_PIN)

# Pick a department to narrow down the choices.
departments = wc.get_exam_departments()
print "Departments: {}".format(", ".join(departments))
department = raw_input("Please enter one of the above departments: ")

while department not in departments:
    department = raw_input("{} is an invalid department. Please enter a valid one: ".format(department))

# Pick a class to download the exams for.
exams = wc.get_exams(department)
courses = list(set([exam.class_name.lower().replace(" ", "") for exam in exams]))
print "Courses: {}".format(", ".join(courses))
course = raw_input("Enter one of the above courses to download: ")

while course not in courses:
    course = raw_input("{} is an invalid course. Please enter a valid one: ".format(course))

# Download all of the exams.
path = raw_input("Please enter a path to a directory to save in: ")
path = os.path.expanduser(path)

while not os.path.exists(path):
    path = raw_input("That doesn't seem to be a valid path. Please enter a valid one: ")
    path = os.path.expanduser(path)

confirm_continue = raw_input("Are you sure you wish to download to {} ? [Y/n]".format(path))
if confirm_continue != "Y":
    print "Exiting..."
else:
    to_download = [exam for exam in exams if exam.class_name.lower().replace(" ", "") == course]

    for exam in to_download:
        if path[-1] != "/": path += "/"
        full_path = "{prefix}{classname}-{year}-{term}.pdf".format(prefix=path, classname=exam.class_name, year=exam.year, term=exam.term)
        exam.download(full_path)
