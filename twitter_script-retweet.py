
# coding: utf-8

# # retweet #tag from people you follow & scrape tweet

# In[1]:


import re
import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

#user = input('username: ')
user = '+923447724960'

#my_password = getpass('Password: ')
my_password = 'trigger890'

search_term = input('search term: ')


# In[2]:


driver = webdriver.Chrome()
driver.maximize_window()

sleep(3)
print('driver initiated')


# In[3]:


driver.get("https://www.twitter.com/login")
sleep(3)
print('website loaded')


# In[4]:


username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
# username.send_keys('ChampMalik3')
username.send_keys(user)


# In[5]:


password = driver.find_element_by_xpath('//input[@name="session[password]"]')
# password.send_keys('hmmd2754')
password.send_keys(my_password)


# In[6]:


password.send_keys(Keys.RETURN)


# In[7]:


#put delay
sleep(3)
search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
search_input.send_keys(search_term)


# In[8]:


search_input.send_keys(Keys.RETURN)
sleep(3)


# In[9]:


filterr = driver.find_elements_by_class_name("r-1p0dtai.r-1ei5mc7.r-1pi2tsx.r-1d2f490.r-crgep1.r-orgf3d.r-t60dpp.r-u8s1d.r-zchlnj.r-ipm5af.r-13qz1uu")
filterr[1].click()
sleep(3)

# <input name="People" type="radio" data-focusable="true" class="r-1p0dtai r-1ei5mc7 r-1pi2tsx r-1d2f490 r-crgep1 r-orgf3d r-t60dpp r-u8s1d r-zchlnj r-ipm5af r-13qz1uu">


# In[10]:


def get_tweet_data(card):
    """Extract data from tweet card"""
    sleep(1)
    try:
        username = card.find_element_by_xpath('.//span').text
    except:
        username=""
    try:
        handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except NoSuchElementException:
        return
    
   
    try:
        comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    except:
        print('comment not found')
        comment=""
    try:
        responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    except:
        print('Responding not found')
        responding=""
    
    text = comment + responding
    
    try:
        reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    except:
        print('reply count not found')
        reply_cnt=""
    try:
        retweet_cnt = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    
    except:
        print('retweet count not found')
        retweet_cnt=""
    try:
        like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text
        print('like count not found')
    except:
        like_cnt=""
    tweet = (username, handle, text, reply_cnt, retweet_cnt, like_cnt)
    
    try:
        rtButtons = card.find_elements_by_xpath("//div[@data-testid='retweet']")
        for rtButton in rtButtons:
            rtButton.click()
            sleep(2)
            confirm = card.find_element_by_xpath("//div[@data-testid='retweetConfirm']")
            confirm.click()
            sleep(2)
    except:
        pass

    
    
    return tweet    


# In[11]:


# get all tweets on the page
data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for card in page_cards[:20]:
        tweet = get_tweet_data(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)
            
    scroll_attempt = 0
    while True:
        # check scroll position
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(2)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1
            
            # end of scroll region
            if scroll_attempt >= 2:
                scrolling = False
                break
            else:
                sleep(2) # attempt another scroll
        else:
            last_position = curr_position
            
            break

# driver.close()


# In[ ]:


with open(search_term+'.csv', 'w', newline='', encoding='utf-8') as f:
    header = ['UserName', 'Handle',  'Text', 'Comments', 'Likes', 'Retweets']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)


# In[ ]:


import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
df = pd.read_csv(search_term+'.csv')


# In[ ]:


df

