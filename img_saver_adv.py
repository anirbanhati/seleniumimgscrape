from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import requests
import base64
ss=time.time()

def downloader(sg,pg,query):
    ds=time.time()
    saved_folder=os.path.join(DownloadLocation,query)
    if not(os.path.exists(saved_folder)):
        os.mkdir(saved_folder)
    # Creating a webdriver instance
    driver = webdriver.Chrome('D:\chromedriver_win32\chromedriver')
    
    # Maximize the screen
    driver.maximize_window()
    
    # Open Google Images in the browser
    driver.get('https://www.google.com/advanced_image_search')
    
    # Finding the search box
    sgbox=driver.find_element(By.XPATH,'//*[@id="xX4UFf"]')
    sgbox.send_keys(sg)
    cbox=driver.find_element(By.XPATH,'//*[@id="CwYCWc"]')
    cbox.send_keys(pg)
    box = driver.find_element("xpath",'//*[@id="mSoczb"]')
    
    # Type the search query in the search box
    box.send_keys(query)
    
    # Pressing enter
    #box.send_keys(Keys.ENTER)
    driver.find_element("xpath",'//*[@id="s1zaZb"]/div[5]/div[10]/div[2]/input[2]').click()
    time.sleep(3)
    # Function for scrolling to the bottom of Google
    # Images results
    try:
        driver.find_element("xpath",'//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button').click()
        time.sleep(3)
    except:
        pass
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
    il=len(driver.find_elements(By.XPATH,'//*[@id="islrg"]/div[1]/div'))
    print(il)
    # Loop to capture and save each image
    print(len(driver.find_elements(By.XPATH,'//*[@id="i7"]/div[1]/span/span/div')))
    for i in range(1, il+1):
        try:
        
            img = driver.find_element("xpath",
                '//*[@id="islrg"]/div[1]/div[' +
            str(i) + ']/a[1]/div[1]/img')
            link=img.get_attribute("src")
            img_data=link
            image_name = saved_folder + '/' + query + str(i) + '.jpg'
            
            #response = requests.get(link)
            if (link.startswith("data:image/")):
                link=link.partition("base64,")[2]
                with open(image_name, 'wb') as fh:
                    fh.write(base64.b64decode(link))
            if(link.startswith("https://")):
                response=requests.get(link)
                with open(image_name, 'wb') as fh:
                    fh.write(response.content)
        
            time.sleep(1)
    
        except:
            
            continue
    #---------------------------- sub cats -------------------------------------------------------------
    ll=len(driver.find_elements(By.XPATH,'//*[@id="i7"]/div[1]/span/span/div'))
    print(ll)
    urls=[]
    for i in range(1,ll+1):
        try:
            divlist=driver.find_element(By.XPATH,f'//*[@id="i7"]/div[1]/span/span/div[{i}]/a')
            urls.append(divlist.get_attribute('href'))
        except:
            continue
    c=0
    for l in urls:
        c+=1
        driver.get(l)
        time.sleep(3)
        scroll_to_bottom()
        il=len(driver.find_elements(By.XPATH,'//*[@id="islrg"]/div[1]/div'))
        print(il)
        for i in range(1, il+1):
            try:
            
                img = driver.find_element("xpath",
                    '//*[@id="islrg"]/div[1]/div[' +
                str(i) + ']/a[1]/div[1]/img')
                link=img.get_attribute("src")
                ni=(1000*c)+i
                image_name = saved_folder + '/' + query + str(ni) + '.jpg'
                
                #response = requests.get(link)
                if (link.startswith("data:image/")):
                    link=link.partition("base64,")[2]
                    with open(image_name, 'wb') as fh:
                        fh.write(base64.b64decode(link))
                if(link.startswith("https://")):
                    response=requests.get(link)
                    with open(image_name, 'wb') as fh:
                        fh.write(response.content)
            
                time.sleep(1)
        
            except:
                
                continue
    #---------------------------- /sub cats ------------------------------------------------------------

    driver.close()
    ee=time.time()
    print(f"time spend={ee-ss}")
if __name__=='__main__':
    ss=time.time()
    DownloadLocation="imgadvblk"
    if not(os.path.exists(DownloadLocation)):
        os.mkdir(DownloadLocation)
        print(f"{DownloadLocation} created")
    print("sg?")
    sg=input()
    print("pg?")
    pg=input()
    query=f"{pg} {sg}"
    downloader(sg,pg,query)
    ee=time.time()
    print(f"totaltime={ee-ss}")