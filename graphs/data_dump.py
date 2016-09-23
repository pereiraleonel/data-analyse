#IMPORTS
import sqlite3
import json

#VARIABLES
dep_list = list()
college_dict = dict()
college_list = list()
file_name = 'data.json'
college_list = list()
college_dictionary = dict()
department_dictionary = dict()
hcc = dict()
email_list = list()
email_list = list()

connection = sqlite3.connect('hccs_staff.sqlite')
cursor = connection.cursor()

colleges = cursor.execute('''select college from Staff group by college limit 4''').fetchall()
for college in colleges:
    departments = cursor.execute('''select department from Staff where college is ? group by department limit 5''',(college[0].__str__(),)).fetchall()
    department_list = list()
    for department in departments:
        emails = cursor.execute('''select email from Staff where department is ? and college is ? order by email asc limit 5''',(department[0].__str__(),college[0].__str__())).fetchall()
        email_list = list()
        for email in emails:
            email_list.append({'name' : email[0].__str__()})       
        department_dictionary = {'name' : department[0].__str__(), 'children' : email_list}
        department_list.append(department_dictionary)
    college_dictionary = {'name' : college[0].__str__(), 'children' : department_list}
    college_list.append(college_dictionary)
hcc = {'name':'hcc.edu','children':college_list}

jdata = json.dumps(hcc)
file_handler = open(file_name,'w')
file_handler.write(jdata)
file_handler.close()
