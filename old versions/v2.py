import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
#import config as config
 
# Path to the Excel file
excel_file_path = '.\priority.csv'
# Read the Excel file using pandas
df = pd.read_csv(excel_file_path)
#extract site_name list from the dataframe
site_list = df['site_name'].tolist()
#we need the unique values 
site_list = set(site_list)

# Specify the path to the ChromeDriver executable
driver_path = '.\chromedriver.exe'
# Set the PATH environment variable to include the directory of the ChromeDriver executable
os.environ['PATH'] += os.pathsep + os.path.dirname(driver_path)

# Create a Chrome webdriver instance
driver = webdriver.Chrome()
 
# Open the Tableau Server website
server = 'https://tableaueur.schneider-electric.com/#/site/'

for site_name in site_list:
    server_name = server + site_name + "/tasks/extractRefreshes" #let's land directly to the tasks page
    driver.get(server_name) #get call (i.e. lands to tableau server)

    #we don't need the login
    ''' 
    # # Login to the website (replace 'username' and 'password' with your actual credentials)
    # username = config.username
    # password = config.password
    
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
    '''
    
    # Wait for the login to complete
    time.sleep(2)
    for i in range(len(df)):
        
        #need to check that we are in the correct site
        if site_name == df['site_name'].iloc[i]: #i.e. the site_name we are considering, is equal to the site_name value of the row

            task_name = df['extract_name'].iloc[i]
            schedule_name = df['schedule_name'].iloc[i]
            priority_new = df['new_priority'].iloc[i]

            # Find and click the desired option
            button_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@aria-colindex='4' and contains(@data-tb-test-id, 'actionsmenu-cell') and preceding-sibling::div[@aria-colindex='3' and contains(., '{0}')] and following-sibling::div[@aria-colindex='6' and contains(., '{1}')]]".format(task_name,schedule_name)
                )
            ))
            button_element.click()
            
            # waiting for the menu to be visible
            dropdown_menu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-tb-test-id='action-menu-TextMenuItem']")))
            # click on the forth element of the list (change priority)
            fourth_item = dropdown_menu.find_element(By.XPATH, "//div[@data-tb-test-id='action-menu-tasks-priority-MenuItem']")
            fourth_item.click()
            
            # find the box
            input_element  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@data-tb-test-id='-IntegerStepperWidget-TextInput']")))
            time.sleep(1)
            # JavaScript to drop the existing element
            driver.execute_script("arguments[0].value = '';", input_element)
            time.sleep(1)
            # insert new element
            input_element.send_keys('{0}'.format(priority_new))
            time.sleep(1)
            
            # find and click on the botton "change priority"
            confirm_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@data-tb-test-id='confirm-action-dialog-confirm-Button']")))
            confirm_button.click()
            
            # Wait for the login to complete
            time.sleep(2)
        
        else: 
            continue

# Close the browser
driver.quit()