import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from time import sleep
import random
import matplotlib.pyplot as plt
import numpy as np
import threading

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value,OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names,operating_systems =operating_systems,limit = 100)
user_agent = user_agent_rotator.get_random_user_agent()
global all_currents
global all_times
global all_bids
global all_asks
all_currents = []
all_times = []
all_bids = []
all_asks = []

def get_data():
    URL = 'https://pl.investing.com/currencies/live-currency-cross-rates'
    while True:
        user_agent = user_agent_rotator.get_random_user_agent()
        request = requests.get(URL,headers = {'User-Agent': user_agent})
    
        cont = BeautifulSoup(request.content, 'html.parser')
        
        tables = cont.find('div', class_ = 'js-cross-rates-table liveCurrencyBoxWrap')
        tables = tables.find_all('div',class_ = 'liveCurrencyBox')
        currents = []
        times = []
        bids = []
        asks = []
        for table in tables:
            current = table.find('div', class_ = 'topBox').a.text
            time = table.find('div', class_ = 'topBox').span.text
            bid_ask = table.find('div',class_ = 'contentBox')
            bid_ask = bid_ask.find_all('div', class_ = 'innerContainerWrap')
            bid = float(bid_ask[0].text.split('\n')[2].replace('.','').replace(',','.'))
            ask = float(bid_ask[1].text.split('\n')[2].replace('.','').replace(',','.'))
            
            currents.append(current)
            times.append(time)
            bids.append(bid)
            asks.append(ask)
        
        all_currents.append(currents)
        all_times.append(times)
        all_bids.append(bids)
        all_asks.append(asks)
        sleep(random.uniform(4.5, 5))
    
    
def prepare_data(currents,times,bids,asks):
    
    times = np.array(times)
    bids = np.array(bids)
    asks = np.array(asks)
    x_axis = np.arange(1,len(bids)+1)
    plt.clf()
    for i in range(3):
        plt.scatter(x_axis,bids[:,i],label = currents[0][i]+ ' BID ')
        plt.plot(x_axis,bids[:,i])
    plt.legend()

def plot_data():
    while True:
        sleep(random.uniform(4.5, 5))
        global all_currents
        global all_times
        global all_bids
        global all_asks
        prepare_data(all_currents,all_times,all_bids,all_asks)
        
    
    
x = threading.Thread(target = get_data) 
x2 = threading.Thread(target = plot_data) 
x.start()
x2.start()


