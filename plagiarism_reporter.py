import selenium
import time
import sys
import csv

from selenium import webdriver
 
micro_sleep = 1.5
small_sleep = 3
sleep = 5
big_sleep = 15

click_element = lambda driver, xpath: driver.find_element_by_xpath(xpath).click()
text_element = lambda driver, xpath, text: driver.find_element_by_xpath(xpath).send_keys(text)
file_element = lambda driver, xpath, filepath: driver.find_element_by_xpath(xpath).send_keys(filepath)
wait = lambda x: time.sleep(x)

initial_url = 'https://intranet.sydney.edu.au/teaching-support/academic-integrity/report-incident.html'

driver = webdriver.Firefox()
driver.get(initial_url)
print("Please Login")
print("Once you have Logged in, Press Enter to Continue")
while input() != '':
    continue


active_element = driver.find_elements_by_class_name('usyd-cta')[2]
active_element.click()
wait(sleep)


# Time to get a file:
if len(sys.argv) < 2:
    print("Please provide a path to a properly formatted csv file containing your plagiarism data.")
    file_name = input()
else:
    file_name = sys.argv[1]

try:
    raw_data = open(file_name, 'r').readlines()
except:
    print("File error")
    exit()

#try:
(code,
 session, 
 task,
 mode,
 turnitin,
 assessment_instructions_url,
 assessment_instructions_file,
 supporting_documentation_file) = raw_data[1].split(',')[:-1] + [''] * (9 - len(raw_data[1].split(',')))
outline = "https://www.sydney.edu.au/units/" + code

cases = []

for element in raw_data[4:]:
    # Separate and pad
    components = element.split(',')[:-1]
    components += [''] * (7 - len(components))

    case = {
        'sid'    : components[0],
        'reason' : components[1],
        'report' : components[2],
        'student_assessment': components[3],
        'turnitin_report'   : components[4],
        'additional_1'      : components[5],
        'additional_2'      : components[6]
         }
    cases.append(case)


# Check if the reason is in this list
possible_reasons = [
"Plagiarism – some attribution",
"Plagiarism – without attribution",
"Peer-to-peer plagiarism or potential collusion",
"Recycling – inappropriate reuse of material",
"Illegitimate sharing of assessment questions or answers",
"Assignment completed by person other than student",
"Other – please specify Reason for Referral",
"Fabricating data, information or sources",
"Inappropriate upload to a file-sharing or online platform",
]
for case in cases:
    if case['reason'] not in possible_reasons:
        print("Inappropriate reason given: ", case['reason'])
        print(possible_reasons)
        exit()      

# except:
#     print("Data Format Error in CSV")
#     exit()



# # This section should read from file
# code = 'INFO2222'
# session = 'Semester 1 (Main)'
# task = 'Logbook'
# mode = 'individual'
# turnitin = 'False'
# assessment_instructions_url = ""
# assessment_instructions_file = ""
# supporting_documentation_file = ""


active_element =  driver.find_element_by_xpath('//*[@id="MainContent_ddTeachingSession"]')
selector = selenium.webdriver.support.select.Select(active_element)
selector.select_by_visible_text(session)

text_element(driver, '//*[@id="MainContent_txtUosCode"]', code)
click_element(driver, '//*[@id="MainContent_butLookupCourseCode"]')
wait(small_sleep) # Wait for page Load

text_element(driver, '//*[@id="MainContent_txtTask"]', task)

# Individual or Group Assessment
if mode == 'individual':
    click_element(driver, '//*[@id="MainContent_optModeIndividual"]')
else:
    click_element(driver, '//*[@id="MainContent_optModeGroupWork"]')

# Turnitin used
if turnitin.lower() == 'true':
    click_element(driver, '//*[@id="MainContent_optTurnitinYes"]')
else:
    click_element(driver, '//*[@id="MainContent_optTurnitinNo"]')

# Unit of Study Outline URL
text_element(driver, 
    '//*[@id="MainContent_txtUoSOutlineURL"]', 
    outline)

# Assessment Instructions URL
if len(assessment_instructions_url) > 0:
    text_element(driver, 
        '//*[@id="MainContent_txtAssessmentURL"]', 
        assessment_instructions_url)

# Assessment Instructions File
if len(assessment_instructions_file) > 0:
    file_element(driver, 
        '//*[@id="MainContent_uplAssessmentInstructionsFile"]', 
        assessment_instructions_file)

# Supporting Documentation File
if len(supporting_documentation_file) > 0:
    file_element(driver, 
        '//*[@id="MainContent_uplSupportingDocument"]', 
        supporting_documentation_file)

wait(small_sleep)

# Next Page
click_element(driver, '//*[@id="MainContent_butNext"]')

wait(small_sleep)
### REPORTING ###

# SIDS
# Enter SIDs
sids = '\n'.join(case['sid'] for case in cases)
text_element(driver, '//*[@id="MainContent_txtSidList"]', sids)

# Press Lookup
click_element(driver, '//*[@id="MainContent_butLookupSidList"]')
print("Taking a short break while everything reloads...")
wait(big_sleep)

for id, case in enumerate(cases):

    active_element =  driver.find_element_by_xpath('//*[@id="MainContent_rptrStudentList_ddAllegedConduct_{id}"]'.format(id=id))
    selector = selenium.webdriver.support.select.Select(active_element)
    selector.select_by_visible_text(case['reason'])

    wait(small_sleep)

    # Because this form is so bad we do this twice to ensure it goes through
    active_element =  driver.find_element_by_xpath('//*[@id="MainContent_rptrStudentList_ddAllegedConduct_{id}"]'.format(id=id))
    selector = selenium.webdriver.support.select.Select(active_element)
    selector.select_by_visible_text(case['reason'])

    wait(small_sleep)

    text_element(driver, 
        '//*[@id="MainContent_rptrStudentList_txtStudentReason_{id}"]'.format(id=id),
        case['report'])
    wait(small_sleep)

# Just to load it once and change the context
file_element(driver, '//*[@id="MainContent_rptrStudentList2_uplAssessment_0"]'.format(id=id),'')

# No sleeps needed here?
wait(small_sleep)
for id, case in enumerate(cases):

    if len(case['student_assessment']) > 0:
        file_element(driver,
            '//*[@id="MainContent_rptrStudentList2_uplAssessment_{id}"]'.format(id=id),
            case['student_assessment'])
        wait(micro_sleep)

    if len(case['turnitin_report']) > 0:
        file_element(driver, 
            '//*[@id="MainContent_rptrStudentList2_uplTurnitinReport_{id}"]'.format(id=id),
            case['turnitin_report'])
        wait(micro_sleep)

    if len(case['additional_1']) > 0:
        file_element(driver, 
            '//*[@id="MainContent_rptrStudentList2_uplStudent1_{id}"]'.format(id=id),
            case['additional_1'])
        wait(micro_sleep)

    if len(case['additional_2']) > 0:
        file_element(driver,
            '//*[@id="MainContent_rptrStudentList2_uplStudent2_{id}"]'.format(id=id),
            case['additional_2'])
        wait(micro_sleep)

print("READY TO LODGE!")
