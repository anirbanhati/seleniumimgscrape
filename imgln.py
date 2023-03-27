from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import requests
import base64
ss=time.time()
# What you enter here will be searched for in
# Google Images
print("query")
query = input()
downloadfolder="imagesln"
saved_folder="thumbsln"
# if not(os.path.exists(downloadfolder)):
#     os.mkdir(downloadfolder)
# downloadfolder=os.path.join(downloadfolder,query)
# if not(os.path.exists(downloadfolder)):
#     os.mkdir(downloadfolder)
if not(os.path.exists(saved_folder)):
    os.mkdir(saved_folder)
saved_folder=os.path.join(saved_folder,query)
if not(os.path.exists(saved_folder)):
    os.mkdir(saved_folder)
# Creating a webdriver instance
driver = webdriver.Chrome('D:\chromedriver_win32\chromedriver')
 
# Maximize the screen
driver.maximize_window()
 
# Open Google Images in the browser
driver.get('https://images.google.com/')
 
# Finding the search box
box = driver.find_element("xpath",'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
 
# Type the search query in the search box
box.send_keys(query)
 
# Pressing enter
box.send_keys(Keys.ENTER)
 
# Function for scrolling to the bottom of Google
# Images results
def scroll_to_bottom():
 
    last_height = driver.execute_script('\
    return document.body.scrollHeight')
 
    while True:
        driver.execute_script('\
        window.scrollTo(0,document.body.scrollHeight)')
 
        # waiting for the results to load
        # Increase the sleep time if your internet is slow
        time.sleep(3)
 
        new_height = driver.execute_script('\
        return document.body.scrollHeight')
 
        # click on "Show more results" (if exists)
        try:
            driver.find_element(By.CSS_SELECTOR,".YstHxe input").click()
 
            # waiting for the results to load
            # Increase the sleep time if your internet is slow
            time.sleep(3)
 
        except Exception as e:
            # print(f"Show more results --{e}")
            pass
        try:
            driver.find_element(By.CSS_SELECTOR,".WYR1I span").click()
 
            # waiting for the results to load
            # Increase the sleep time if your internet is slow
            last_height+=1
            time.sleep(3)
 
        except Exception as e:
            # print(f"Show more results --{e}")
            pass
 
        # checking if we have reached the bottom of the page
        if new_height == last_height:
            break
 
        last_height = new_height
 
 
# Calling the function
 
# NOTE: If you only want to capture a few images,
# there is no need to use the scroll_to_bottom() function.
scroll_to_bottom()
print(len(driver.find_elements(By.XPATH,'//*[@id="islrg"]/div[1]/div')))
img = driver.find_element("xpath",
            '//*[@id="islrg"]/div[1]/div[' +
          str(len(driver.find_elements(By.XPATH,'//*[@id="islrg"]/div[1]/div'))) + ']/a[1]/div[1]/img')
link=img.get_attribute("src")
img_data=link
image_name = saved_folder + '/' + query + str(len(driver.find_elements(By.XPATH,'//*[@id="islrg"]/div[1]/div'))) + '.jpg'
response = requests.get(link)
if (link.startswith("data:image/jpeg;base64,")):
    link=link.replace("data:image/jpeg;base64,","")
    with open(image_name, 'wb') as fh:
        fh.write(base64.b64decode(link))
if(link.startswith("https://")):
    response=requests.get(link)
    with open(image_name, 'wb') as fh:
        fh.write(response.content)
# Loop to capture and save each image
# for i in range(1, 1000):
#     try:
        
#         img = driver.find_element("xpath",
#             '//*[@id="islrg"]/div[1]/div[' +
#           str(i) + ']/a[1]/div[1]/img')
#         link=img.get_attribute("src")
#         img_data=link
#         image_name = saved_folder + '/' + query + str(i+1) + '.jpg'
        
#         #response = requests.get(link)
#         if (link.startswith("data:image/jpeg;base64,")):
#             link=link.replace("data:image/jpeg;base64,","")
#             with open(image_name, 'wb') as fh:
#                 fh.write(base64.b64decode(link))
#         if(link.startswith("https://")):
#             response=requests.get(link)
#             with open(image_name, 'wb') as fh:
#                 fh.write(response.content)
       
#         time.sleep(1)
 
#     except:
         
#         continue

driver.close()
ee=time.time()
print(f"time spend={ee-ss}")