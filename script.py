import json
import sys
import csv
import copy

# converts csv with student, class and grades information into a json
# calculates students grade in class and average class grade

# inputs in command line path to course.csv, students.csv, test.csv, marks.csv and output file
def summation():

    coursescsv = sys.argv[1]
    studentscsv = sys.argv[2]
    testscsv = sys.argv[3]
    markscsv = sys.argv[4]
    outputjson = open(sys.argv[5],'w')

    master = {'students': []}
    courses = {'courses': []}
    tests = {'tests':[]}
    marks = {'marks': []}

    reader(studentscsv, master['students'])
    reader(coursescsv, courses['courses'])
    reader(testscsv,tests['tests'])
    reader(markscsv, marks['marks'])

    for i in master['students']:
        i["courses"] = []

    markcheck(tests,outputjson)
    calcgrades(master, courses, tests, marks)

    outputjson.write(json.dumps(master, indent=4))
    outputjson.close()

# calulates average grade in class then students term average
# round grade to two decimal places
def calcgrades(master, courses, tests, marks):
    grade = 0
    course_id = '1'
    student = '1'
    for i in marks.get('marks'):
        temp_course_id = courses["courses"][int(tests['tests'][int(i['test_id']) - 1]['course_id']) - 1]['id']
        if temp_course_id != course_id:
            master['students'][int(student) - 1]['courses'].append(copy.deepcopy(courses['courses'])[int(course_id) - 1])
            master['students'][int(student) - 1]['courses'][len(master['students'][int(student) - 1]['courses']) - 1]['courseAverage'] = round(grade, 2)
            student = i['student_id']
            course_id = temp_course_id
            grade = 0

        grade += int(i['mark']) * int(tests['tests'][int(i['test_id']) - 1]['weight']) / 100
    master['students'][int(student) - 1]['courses'].append(copy.deepcopy(courses['courses'])[int(course_id) - 1])
    master['students'][int(student) - 1]['courses'][len(master['students'][int(student) - 1]['courses']) - 1][
        'courseAverage'] = round(grade, 2)

    for i in master['students']:
        sum = 0
        count = 0
        for j in i['courses']:
            sum += j['courseAverage']
            count += 1
        i['totalAverage'] = round(sum / count, 2)

# check if the test weights for each class equal a hundred
# if they do not print error message and exit
def markcheck(tests, outputjson):
    sum = 0
    id = '1'
    for i in tests.get('tests'):
        if i.get('course_id') != id:
            if sum != 100:
                error(outputjson)
            sum = 0
        sum += int(i['weight'])
        id = i['course_id']

    if sum != 100:
        error(outputjson)


def error(outputjson):
    outputjson.write(json.dumps({'error': "Invalid course weights"}, indent=4))
    outputjson.close()
    exit()


def reader(input, ouput):
    with open(input, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            ouput.append(row)

if __name__ == "__main__":
    summation()
