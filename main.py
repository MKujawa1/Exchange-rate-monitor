import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from time import sleep
import random
import threading

### Generate random user agent
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value,OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names,operating_systems =operating_systems,limit = 100)

def get_data():
    '''
    Get data from page. Print after scraping.

    '''
    ### Page to scraping
    URL = 'https://pl.investing.com/currencies/live-currency-cross-rates'
    ### Init stop variable to break threading
    global stop
    stop = 0
    ### i value to change state in while loop
    i = 0
    while True:
        ### Print names of columns
        if i == 0:
            print('\nCurrent time bid ask')
        ### Get user agent and request
        user_agent = user_agent_rotator.get_random_user_agent()
        request = requests.get(URL,headers = {'User-Agent': user_agent})
        ### Get main data from page and tables
        cont = BeautifulSoup(request.content, 'html.parser')
        tables = cont.find('div', class_ = 'js-cross-rates-table liveCurrencyBoxWrap')
        tables = tables.find_all('div',class_ = 'liveCurrencyBox')
        ### Get elements from each table
        for table in tables:
            current = table.find('div', class_ = 'topBox').a.text
            time = table.find('div', class_ = 'topBox').span.text
            bid_ask = table.find('div',class_ = 'contentBox')
            bid_ask = bid_ask.find_all('div', class_ = 'innerContainerWrap')
            bid = float(bid_ask[0].text.split('\n')[2].replace('.','').replace(',','.'))
            ask = float(bid_ask[1].text.split('\n')[2].replace('.','').replace(',','.'))
            print(current, time,bid,ask)
        ### Wait for change on page 
        sleep(random.uniform(4.5, 5))
        ### Change state
        i+=1
        if i == 1:
            i = 0
        ### While loop break
        if stop == 1:
            break
        
def start():
    '''
    Init threading and while loop to break all loops

    '''
    ### Get Tread object and start threading
    proc = threading.Thread(target = get_data) 
    proc.start()
    ### Loop for break all loops 
    while True:
        ### Init stop value
        global stop 
        ### Get value from user
        stop = int(input('Pass 1 to break: '))
        ### Break loop
        if stop == 1:
            break

### Run
if __name__ == '__main__':
    start()