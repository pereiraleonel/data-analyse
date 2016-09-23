#IMPORTS
from selenium import webdriver
from time import sleep
import sqlite3

#VARIABLES
url = 'http://www.hccs.edu/district/faculty/'
rows = list()
records_retrieved = list()

#METHODS
def examine_records(records):
	current_records = records.split()[1].split('-')
	last_record = int(records.split()[3])
	records_per_page = int(current_records[1])-int(current_records[0]) + 1
	last_page = last_record / records_per_page + 1
	current_page = int(current_records[1])/ records_per_page
	return [current_page,records_per_page,last_page]

#ENGINE
browser = webdriver.Firefox()
browser.get(url)
browser.find_elements_by_id('searchID')[0].click()
records = browser.find_elements_by_xpath('/html/body/div[2]/div/div[2]/article/form/div/table[3]/tbody/tr[2]/td')[0].text
last_page = examine_records(records)[-1]

for i in range(last_page):
    element = browser.find_elements_by_xpath('/html/body/div[2]/div/div[2]/article/form/div/table[2]')
    lines = element[0].find_elements_by_tag_name('tr')
    for counter,line in enumerate(lines):
        if counter == 0: continue #columns = line.find_elements_by_tag_name('th')
        if counter != 0: columns = line.find_elements_by_tag_name('td')
        row = list()
        for column in columns:
            row.append(column.text)
        rows.append(row)
        row
    records_retrieved.append(browser.find_elements_by_xpath('/html/body/div[2]/div/div[2]/article/form/div/table[3]/tbody/tr[2]/td')[0].text)
    records_retrieved[-1],len(rows)
    browser.find_elements_by_name('JumpToNext')[0].click()
    sleep(5)

connection = sqlite3.connect('hccs_staff.sqlite')
cursor = connection.cursor()
cursor.execute('''DROP TABLE IF EXISTS Staff ''')
#cursor.execute('''CREATE TABLE IF NOT EXISTS Staff (first_name TEXT , last_name TEXT, title TEXT, department TEXT, phone TEXT, email TEXT, mail_code TEXT, college TEXT, PRIMARY KEY(email))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Staff_all (first_name TEXT , last_name TEXT, title TEXT, department TEXT, phone TEXT, email TEXT, mail_code TEXT, college TEXT)''')
for counter,row in enumerate(rows):
    cursor.execute('INSERT OR IGNORE INTO Staff_all (first_name,last_name,title,department,phone,email,mail_code,college) VALUES ( ?,?,?,?,?,?,?,? )', ( row[0],row[1],row[2], row[3], row[4], row[5], row[6], row[7] ) )
    row
    if counter % 10 == 0:connection.commit()
    sleep(0.1)
connection.commit()

#293 of 627 2921-2930 of 6267
#SELECT first_name, last_name, title, department, phone, email, mail_code, college FROM Staff_all WHERE email IN  (SELECT email FROM Staff_all   GROUP BY email HAVING COUNT (email) >1) order by email asc


records = browser.find_elements_by_xpath('/html/body/div[1]/div/div[2]/article/form/div/table[3]/tbody/tr[2]/td')[0].text
records = u'Records 11-20 of 6244'
current_records = records.split()[1].split('-')
last_record = int(records.split()[3])
records_per_page = int(current_records[1])-int(current_records[0]) + 1
last_page = last_record / records_per_page + 1
current_page = int(current_records[1])/ records_per_page
if current_page == 1:
    cp = browser.find_elements_by_xpath('/html/body/div[1]/div/div[2]/article/form/div/table[3]/tbody/tr[1]/td[2]/table/tbody/tr/td[2]/input')#page1
if current_page > 1:
    cp = browser.find_elements_by_xpath('/html/body/div[1]/div/div[2]/article/form/div/table[3]/tbody/tr[1]/td[2]/table/tbody/tr/td[4]/input')#page2-n
v = cp[0].get_attribute('value')
cp[0].clear()
cp[0].send_keys(current_page)
cp[0].send_keys(webdriver.common.keys.Keys.RETURN)

#---------------------------------------------------------------
browser = webdriver.Firefox()
browser.get(url)
browser.find_elements_by_id('searchID')[0].click()

while True:
    pages_to_retrieve = int(raw_input('HOW MANY PAGES - '))
    if pages_to_retrieve <= 0:continue
    #
    records = browser.find_elements_by_xpath('/html/body/div[1]/div/div[2]/article/form/div/table[3]/tbody/tr[2]/td')[0].text
    current_records = records.split()[1].split('-')
    last_record = int(records.split()[3])
    records_per_page = int(current_records[1])-int(current_records[0]) + 1
    last_page = last_record / records_per_page + 1
    current_page = int(current_records[1])/ records_per_page
    #
    for i in range(pages_to_retrieve):
        element = browser.find_elements_by_xpath("/html/body/div[1]/div/div[2]/article/form/div/table[2]")
        lines = element[0].find_elements_by_tag_name('tr')
        for counter,line in enumerate(lines):
            if counter == 0: continue #columns = line.find_elements_by_tag_name('th')
            if counter != 0: columns = line.find_elements_by_tag_name('td')
            row = list()
            for column in columns:
                row.append(column.text)
            rows.append(row)
            row
        records_retrieved.append(browser.find_elements_by_xpath('/html/body/div[1]/div/div[2]/article/form/div/table[3]/tbody/tr[2]/td')[0].text)
        #records_retrieved[-1]
        browser.find_elements_by_name('JumpToNext')[0].click()
        sleep(5)
#
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui
from selenium.webdriver.support.ui import WebDriverWait
e = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,'lst-ib')))
browser.implicitly_wait(10)
