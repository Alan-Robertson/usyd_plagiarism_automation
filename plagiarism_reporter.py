import selenium
import time
import sys
import csv

from selenium import webdriver

sleep_time = 5

click_element = lambda driver, xpath: driver.find_element_by_xpath(xpath).click()
text_element = lambda driver, xpath, text: driver.find_element_by_xpath(xpath).send_keys(text)
wait = lambda: time.sleep(sleep_time)


initial_url = 'https://intranet.sydney.edu.au/teaching-support/academic-integrity/report-incident.html'

driver = webdriver.Firefox()
driver.get(initial_url)
print("Please Login")
print("Once you have Logged in, Press Enter to Continue")
while input() != '':
    continue


active_element = driver.find_elements_by_class_name('usyd-cta')[2]
active_element.click()
wait()

code = 'INFO2222'
session = 'Semester 1 (Main)'
task = 'Logbook'
mode = 'individual'
turnitin = 'False'
outline = "https://www.sydney.edu.au/units/" + code

active_element =  driver.find_element_by_xpath('//*[@id="MainContent_ddTeachingSession"]')
selector = selenium.webdriver.support.select.Select(active_element)
selector.select_by_visible_text(session)

text_element(driver, '//*[@id="MainContent_txtUosCode"]', code)
click_element(driver, '//*[@id="MainContent_butLookupCourseCode"]')
wait() # Wait for page Load

text_element(driver, '//*[@id="MainContent_txtTask"]', task)

if mode == 'individual':
    click_element(driver, '//*[@id="MainContent_optModeIndividual"]')
else:
    click_element(driver, '//*[@id="MainContent_optModeGroupWork"]')

if turnitin == 'True':
    click_element(driver, '//*[@id="MainContent_optTurnitinYes"]')
else:
    click_element(driver, '//*[@id="MainContent_optTurnitinNo"]')

text_element(driver, '//*[@id="MainContent_txtUoSOutlineURL"]', outline)
