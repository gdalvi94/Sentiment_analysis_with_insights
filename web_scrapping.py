from selenium import webdriver
import time
import pandas as pd
import sqlite3 as sql

driver=webdriver.Chrome()
url="https://www.etsy.com/in-en/listing/846918572/capricorn-constellation-ring-with?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=pagination&plkey=7a19c83064c67954653b93b95c45fae8f56fcc45%3A846918572&pro=1"
driver.get(url)
condition=True
i=2
a=[]
while condition:
        if i<4 or i>50:
            kk= driver.find_element_by_css_selector('#reviews > div.wt-flex-xl-5.wt-flex-wrap > nav > ul > li:nth-child(6) > a')
        else:
            kk= driver.find_element_by_css_selector('#reviews > div.wt-flex-xl-5.wt-flex-wrap > nav > ul > li:nth-child(7) > a')

        try:
            if kk.get_attribute('data-page')== str(i):
                for j in range(0,4):
                    try:
                        a.append(driver.find_element_by_css_selector("#review-preview-toggle-"+str(j)).text)
                    except:
                        pass
                kk.click()
                time.sleep(3)
                i = i+1
                print(i)
                if i==52:
                    for j in range(0,4):
                        try:
                            a.append(driver.find_element_by_css_selector('#review-preview-toggle-'+str(j)).text)
                        except:
                            pass
                    
                    condition=False
           
            else:
                pass
        except:
            condition=False
driver.close()  
df = pd.DataFrame()

df['reviews'] =  a
# Dataframe to csv
df.to_csv('reviews.csv', index = False)
conn = sql.connect('reviews.db')
#To SQL
df.to_sql('reviewtbl', conn)


#load the database table back to dataframe
conn = sql.connect('reviews.db')
new_df = pd.read_sql('SELECT * FROM reviewtbl',conn)
