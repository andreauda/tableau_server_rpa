import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import logging
import datetime as datetime
 
# Logger Configuration
today_date = datetime.datetime.now().strftime(f'%Y-%m-%d')
log_filename = f'logs/log_{today_date}.log'
logging.basicConfig(filename=log_filename, 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('''
             
             SCRIPT STARTED...
             ''')

# Open the Tableau Server website
server = 'https://tableau.schneider-electric.com/#/site/'

try:
    # Path to the Excel file
    excel_file_path = '.\priority_files\priority_sampled.csv'
    # Read the Excel file using pandas
    df = pd.read_csv(excel_file_path)
    #extract site_name list from the dataframe (only unique values)
    site_list = df['site_urlname'].unique().tolist()
    logging.info('csv file imported')
except Exception as e:
    logging.error('error with csv file: {0}'.format(e))

try:
    # Specify the path to the ChromeDriver executable
    driver_path = '.\chromedriver.exe'
    # Set the PATH environment variable to include the directory of the ChromeDriver executable
    os.environ['PATH'] += os.pathsep + os.path.dirname(driver_path)
    # Create a Chrome webdriver instance
    driver = webdriver.Chrome()
    logging.info('chromedriver is working fine')
except Exception as e:
    logging.error('error with chromedriver: {0}'.format(e))

for site_name in site_list:
    try:
        server_name = server + site_name + "/tasks/extractRefreshes" #let's land directly to the tasks page
        driver.get(server_name) #get call (i.e. lands to tableau server)
        time.sleep(2)         
        driver.execute_script("""document.body.style.zoom='25%'""")
        # time.sleep(5)
        logging.info('site: {1},: {0}'.format(server_name, site_name))
    except:
        logging.error('NOT connected to site: {0}'.format(site_name))

        
    # Wait for the login to complete
    time.sleep(2)
    for i in range(len(df)):
        
        #need to check that we are in the correct site
        if site_name == df['site_urlname'].iloc[i]: #i.e. the site_name we are considering, is equal to the site_name value of the row
            task_name = df['extract_name'].iloc[i]
            schedule_name = df['schedule_name'].iloc[i]
            priority_new = df['new_priority'].iloc[i]
            priority_old = df['old_priority'].iloc[i]

            #the priority must be different
            if df['old_priority'].iloc[i] != df['new_priority'].iloc[i]:



                try:
                    # Find and click the desired option
                    button_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                        (By.XPATH, "//div[@aria-colindex='4' and contains(@data-tb-test-id, 'actionsmenu-cell') and preceding-sibling::div[@aria-colindex='3' and contains(., '{0}')] and following-sibling::div[@aria-colindex='6' and contains(., '{1}')]]".format(task_name,schedule_name)
                        )
                    ))
                    button_element.click()
                    time.sleep(2)
                    
                    # waiting for the menu to be visible
                    dropdown_menu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-tb-test-id='action-menu-TextMenuItem']")))
                    # click on the forth element of the list (change priority)
                    fourth_item = dropdown_menu.find_element(By.XPATH, "//div[@data-tb-test-id='action-menu-tasks-priority-MenuItem']")
                    fourth_item.click()
                    time.sleep(2)
                    
                    # find the box                    
                    input_element  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@data-tb-test-id='-IntegerStepperWidget-TextInput']")))
                    # JavaScript to drop the existing element
                    driver.execute_script("arguments[0].value = '';", input_element)
                    time.sleep(2)
                    
                    # insert new element
                    input_element.send_keys('{0}'.format(priority_new))
                    time.sleep(2)
                    
                    # find and click on the botton "change priority"
                    confirm_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@data-tb-test-id='confirm-action-dialog-confirm-Button']")))
                    confirm_button.click()
                    time.sleep(2)

                    logging.info('priority from {3}, to {4}, row {0} - extract "{1}", schedule: "{2}" '.format(i+1, task_name, schedule_name, priority_old, priority_new))

                except Exception as e:
                    logging.error('row {3}, priority not changed for row {0} - extract "{1}", schedule: "{2}"'.format(i+1, task_name, schedule_name, e))
            
            else:
                logging.info('not changes requiredd for row {0}: old_priority = new_priority, extract "{1}"'.format(i+1, task_name))
                continue
                

        else: 
            continue

try:
    # Close the browser
    driver.quit()
    logging.info('browser closed, script ends')
except Exception as e:
    logging.error('browser NOT closed')
    
