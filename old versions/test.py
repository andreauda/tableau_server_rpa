import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import config as config

# Path to the Excel file
excel_file_path = '.\priority.csv'

# Read the Excel file using pandas
df = pd.read_csv(excel_file_path)

# Specify the path to the ChromeDriver executable
driver_path = '.\chromedriver.exe'

# Set the PATH environment variable to include the directory of the ChromeDriver executable
os.environ['PATH'] += os.pathsep + os.path.dirname(driver_path)

# Create a Chrome webdriver instance
driver = webdriver.Chrome()

# Open the Tableau Server website
driver.get(config.server)

# Login to the website (replace 'username' and 'password' with your actual credentials)
username = config.username
password = config.password

# ###login
# username_field = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/span[1]/form[1]/div[1]/div[1]/div[1]/div[1]/input[1]'))
# )
# username_field.send_keys(username)
# time.sleep(1)

# password_field = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/span[1]/form[1]/div[1]/div[2]/div[1]/div[1]/input[1]'))
# )
# password_field.send_keys(password)
# time.sleep(1)

# signin_button = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))
# )
# signin_button.click()

# Wait for the login to complete
time.sleep(2)

'''
# # Iterate over the rows in the Excel file
# for index, row in df.iterrows():
#     extract_name = row['extract_name']
#     schedule_name = row['schedule_name']
#     old_priority = row['old_priority']
#     new_priority = row['new_priority']
'''

task_schedule_name = "test_extract_refresh"
# Find and click the desired option
row_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@data-tb-test-id, 'extractTaskName-cell') and contains(., '{0}')]".format(task_schedule_name))))
button_element = row_element.find_element(By.XPATH, "./following-sibling::div[@data-tb-test-id='actionsmenu-cell']//button[@data-tb-test-id='action-menu-Button']")
button_element.click()

# waiting for the menu to be visible
dropdown_menu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-tb-test-id='action-menu-TextMenuItem']")))
# click on the forth element
fourth_item = dropdown_menu.find_element(By.XPATH, "//div[@data-tb-test-id='action-menu-tasks-priority-MenuItem']")
fourth_item.click()

# find the element
input_element  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@data-tb-test-id='-IntegerStepperWidget-TextInput']")))
time.sleep(1)
# JavaScript to drop the existing element
driver.execute_script("arguments[0].value = '';", input_element)
# insert new element
input_element.send_keys('75')

# find and click on the botton "change priority"
time.sleep(2)
confirm_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@data-tb-test-id='confirm-action-dialog-confirm-Button']")))
confirm_button.click()

# Wait for the login to complete
time.sleep(5)
# Close the browser
driver.quit()