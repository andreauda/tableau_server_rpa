import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import logging
import datetime as datetime
 
# Logger Configuration
today_date = datetime.datetime.now().strftime(f'%Y-%m-%d')
log_filename = f'logs/logV3_{today_date}.log'
logging.basicConfig(filename=log_filename, 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('''
             
             SCRIPT STARTED...
             ''')

# Open the Tableau Server website
server = 'https://tableau.schneider-electric.com/#/'

#Reading the .csv file 
try:
    excel_file_path = '.\priority_files\priority.csv' # Path
    df = pd.read_csv(excel_file_path)
    logging.info('csv file imported')
except Exception as e:
    logging.error('error with csv file: {0}'.format(e))

#Set the cheromedriver.exe 
try:
    driver_path = '.\chromedriver.exe' #path 
    # Set the PATH environment variable to include the directory of the ChromeDriver executable
    os.environ['PATH'] += os.pathsep + os.path.dirname(driver_path)
    driver = webdriver.Chrome() # Create a Chrome webdriver instance
    logging.info('chromedriver is working fine')
except Exception as e:
    logging.error('error with chromedriver: {0}'.format(e))

for index, row in df.iterrows():
    #creating the url based on the info provided in the .csv
    if row['site_name'] != 'Enterprise BI':
        url = server + 'site/' + row['site_urlname'] + '/' + row['content_type'] + '/' + str(row['id_url']) + '/extractRefreshes'
    #the url for Enterprise BI is different
    else:
        url = server + row['content_type'] + '/' + str(row['id_url']) + '/extractRefreshes'
    
    #costant values for the loop
    schedule_name = row['schedule_name']
    priority_new = row['new_priority']

    driver.get(url)
    time.sleep(2) 
    logging.info('row {0} - landed to: {1}'.format(index+1, url))
    
    actions_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@aria-colindex='3' and contains(@data-tb-test-id, 'actionsmenu-cell') and following-sibling::div[@aria-colindex='4' and contains(., '{0}')]]".format(schedule_name)
            )
        )
    )
    actions_button.click()
    time.sleep(1)
    logging.info('cliked on the actionsmenu-cell'.format(index+1))

    # waiting for the menu to be visible
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@data-tb-test-id='action-menu-TextMenuItem']"
                )
        )
    )
    # click on the forth element of the list (change priority)
    fourth_item = dropdown_menu.find_element(
        By.XPATH, "//div[@data-tb-test-id='action-menu-tasks-priority-MenuItem']"
        )
    fourth_item.click()
    time.sleep(1)
    logging.info('cliked on the action-menu-tasks-priority-MenuItem')

    #             #delete the old priority
    #             try:
    #                 # find the box                    
    #                 input_element  = WebDriverWait(driver, 10).until(
    #                     EC.visibility_of_element_located(
    #                         (By.XPATH, "//input[@data-tb-test-id='-IntegerStepperWidget-TextInput']")
    #                     )
    #                 )
    #                 # JavaScript to drop the existing element
    #                 driver.execute_script("arguments[0].value = '';", input_element)
    #                 time.sleep(1)
    #                 logging.info('old priority deleted')

    #                 #insert the new priority
    #                 try:
    #                     input_element.send_keys('{0}'.format(priority_new))
    #                     time.sleep(1)
    #                     logging.info('priority changed, waiting for confirming click')

    #                     # find and click on the botton "change priority"
    #                     try:
    #                         confirm_button = WebDriverWait(driver, 10).until(
    #                             EC.visibility_of_element_located(
    #                                 (By.XPATH, "//button[@data-tb-test-id='confirm-action-dialog-confirm-Button']")
    #                             )
    #                         )
    #                         confirm_button.click()
    #                         logging.info('priority changed, confirming click done')
    #                     except Exception as e:
    #                         logging.error('priority changed, confirming click NOT done')

    #                 except Exception as e:
    #                     logging.error('priority NOT changed, error {0}'.format(e))

    #             except Exception as e:
    #                 logging.error('old priority NOT deleted, error {0}'.format(e))

    #         except Exception as e:
    #             logging.error('NOT cliked on the action-menu-tasks-priority-MenuItem, error {0}'.format(e))

    #     except Exception as e:
    #         logging.error('NOT cliked on the actionsmenu-cell button, error {0}'.format(e))

    # except Exception as e:
    #     logging.error('row {0} - url not reached, error: {1}'.format(index+1, e))

try:
    # Close the browser
    driver.quit()
    logging.info('browser closed, script ends')
except Exception as e:
    logging.error('browser NOT closed')