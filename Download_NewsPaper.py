#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import warnings
warnings.filterwarnings("ignore")
import datetime


# In[4]:


def link_to_ET():
    desired_link = None
    url1 = "https://dailyepaper.in/economic-times-newspaper-today/"
    page = requests.get(url1, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    for p in soup.find_all('p'):
        pattern = ': Download Now'
        result = p.text.find(pattern)
        if result!=-1:
            desired_p = p 
            desired_link = desired_p.find('a')['href']
            break
    r_l = requests.get(desired_link, stream=True,allow_redirects=True,verify=False)
    soup_l = BeautifulSoup(r_l.content, 'html.parser')
    src_link = soup_l.find('iframe')['src'].split('?')[0]
    return src_link

def link_to_Hindu():
    url = "https://www.e-employmentnews.co.in/the-hindu-pdf/"
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    latest_row = 1
    link_to_download = soup.find_all('table')[3].find('tbody').find_all('tr')[latest_row].find_all('td')[1].find('a')['href']
    return link_to_download

def send_message(bot_token,bot_chatID):
    link_to_hindu = link_to_Hindu()
    link_to_ETimes = link_to_ET()
    send_hindu(link_to_hindu,bot_token,bot_chatID)
    send_ET(link_to_ETimes,bot_token,bot_chatID)
        
def send_hindu(link,token,id):
    send_text = "https://api.telegram.org/bot"+token+'/sendMessage?chat_id='+ id + "&text=" + link
    response = requests.get(send_text)
    print("The Hindu has been sent.")
    
def send_ET(src,token,id):
    r = requests.get(src, stream=True,allow_redirects=True,verify=False)
    file_name = "ET_Times_" +datetime.datetime.today().strftime("%d_%m_%Y_%H_%M_%S")+ ".pdf"
    w_file = open(file_name, 'wb')
    w_file.write(r.content)
    read_files = open(file_name,'rb')
    send_text = "https://api.telegram.org/bot"+token+'/sendDocument?chat_id='+ id + "&caption=" 
    files = {'document':read_files}
    requests.post(send_text,files=files)
    print("ET has been sent.")


# In[5]:


if __name__  == "__main__":
    names = ['Abhay','Anurag']
    bot_chatID = ["894806951","766224475"]
    bot_token = ["1873225189:AAFww-fLV_bYHc01hYKyf7mubHt3o5PB7uE","1820059069:AAH5OzQUS8FGnrnkMZ0L_T0udbZQ08UmrTE"]
    for token,c_id,name in zip(bot_token,bot_chatID,names):
        print("Sending To ",name,'\n')
        send_message(token,c_id)


# In[ ]:




