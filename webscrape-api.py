#!/usr/bin/env python
from bs4 import BeautifulSoup
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()
import sys

import speedtest
from time import gmtime, strftime
import time
import datetime
from itertools import chain
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import matplotlib.ticker as ticker
import math
import os
import re
import json
import requests
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import shutil

#Get current IP for IPS information

global driver
driver = webdriver.Firefox()

class scrape:

	def __init__(self):
		driver.get('http://beta.speedtest.net/')
		time.sleep(10)
		driver.find_element_by_xpath(".//*[@id='container']/div[2]/div/div/div/div[3]/div[1]/div[1]/a/span[3]").click()
		for self.seconds in range(1,61):
			time.sleep(1)
			print ("Testing connection " + str(self.seconds))
		self.html_source = driver.page_source
		self.soup = BeautifulSoup(self.html_source,'html.parser')  		
		self.results = self.soup.findAll('div',{'class':'result-container-speed'})  
		self.up = self.soup.findAll('span',{'class':'result-data-large number result-data-value upload-speed'})[0].text
		self.down = self.soup.findAll('span',{'class':'result-data-large number result-data-value download-speed'})[0].text
		self.ping = self.soup.findAll('span',{'class':'result-data-large number result-data-value ping-speed'})[0].text
		self.ping = self.soup.findAll('span',{'class':'result-data-large number result-data-value ping-speed'})[0].text
		self.ispname = self.soup.findAll('div',{'class':'result-label'})
		self.city = self.soup.findAll('span',{'class':'name'})[0].text
		self.isp = self.ispname[5].text
		
def main():
	ping_time=[]
	ping_time_st=[]
	
	upspeed=[]
	upspeed_st=[]
	
	downspeed=[]
	downspeed_st = []
	
	time_now =[]
	counter = 0
	

	
	while True:
		try:
			
			speettest = scrape()
			counter += 1
			if counter == 25:
				timestr = str(time.strftime("%d-%m-%Y"))
				shutil.copy("speed.png", timestr + ".png")
				counter = 0
				
			# If you want to test against a specific server visit https://www.speedtestserver.com/
			# and find a server you want to test with e.g. servers = [2627] which is Perth
			servers = [2627]

			s = speedtest.Speedtest()
			s.get_servers(servers)
			s.get_best_server()
			s.download()
			s.upload()

			results_dict = s.results.dict()

			download_now = float(round(results_dict['download']/1000000,2))
			upload_now = float(round(results_dict['upload']/1000000,2))
			ping_now = float(round(results_dict['ping'],2))
			
			downspeed.append(download_now)
			upspeed.append(upload_now)
			ping_time.append(ping_now)
			time_now.append(time.strftime("%I %p"))
			
			downspeed_st.append(float(speettest.down))
			upspeed_st.append(float(speettest.up))
			ping_time_st.append(float(speettest.ping))
			
	
			if len(downspeed) >= 25:
				del downspeed[0],downspeed_st[0],upspeed[0],upspeed_st[0],ping_time[0],ping_time_st[0],time_now[0]
				
				
			maxdl = round(max(downspeed+downspeed_st))
			mindl = round(min(downspeed+downspeed_st))
			maxup = round(max(upspeed+upspeed_st))
			minup = round(min(upspeed+upspeed_st))
			maxping = round(max(ping_time+ping_time_st))
			minping = round(max(ping_time+ping_time_st))
			

			x = np.arange(1,len(time_now)+1)								
			fig, ax1 = plt.subplots()
			plt.grid()							
			ax1.plot(x, downspeed, c='#FF6347', label='Down speed API')		
			ax1.set_xlabel("{} - {} - {}\nOokla MAX\MIN - Down {}\{} - Up {}\{} - Ping {}\{} ms\nAPI MAX\MIN - Down {}\{} - Up {}\{} - Ping {}\{} ms"\
			.format(str(speettest.isp),str(speettest.city),str(time.strftime("%d-%m-%Y")),\
			max(downspeed_st),min(downspeed_st),max(upspeed_st),min(upspeed_st),max(ping_time_st),min(ping_time_st)\
			,max(downspeed),min(downspeed),max(upspeed),min(upspeed),max(ping_time),min(ping_time)))
			ax1.set_ylabel('Down Speed', color='#FF6347')	
			ax1.tick_params('y', colors='#FF6347')	
			if abs(max(downspeed)-min(downspeed)) > 20:
				ax1.set_yticks(np.arange(mindl -20, maxdl +3,4))
			else:
				ax1.set_yticks(np.arange(mindl -20, maxdl +3,2))
			ax1.set_xticklabels( time_now, rotation=45 )		
			plt.xticks(x,time_now)								
			
			
			
			ax2 = ax1.twinx()								## ADD another plot
			ax2.plot(x, upspeed, label='Up Speed API')
			ax2.set_ylabel('Up Speed', color='b')
			ax2.tick_params('y', colors='b')
			if abs(max(upspeed)-min(upspeed)) > 20:
				ax2.set_yticks(np.arange(minup -10, maxup +13,4))
			else:
				ax2.set_yticks(np.arange(minup -10, maxup +13,2))

			ax3 = ax1.twinx()								## ADD another plot
			ax3.plot(x, ping_time, c = '#006400', linestyle=':',label='Ping API')
			ax3.set_ylabel('Ping', color='#006400')
			ax3.tick_params('y', colors='#006400')
			ax3.set_yticks(np.arange(0, maxping +150,10))
			ax3.spines['right'].set_position(('axes', 1.15))
			
			ax4 = ax1.twinx()								## ADD another plot
			ax4.plot(x, ping_time_st, c = '#000000', linestyle=':',label='Ookla Ping')
			ax4.set_yticks(np.arange(0, maxping +150,10))
			ax4.set_yticklabels([])
			ax4.tick_params(right="off")
			
			
			ax5 = ax1.twinx()								## ADD another plot
			ax5.plot(x, upspeed_st, c = '#000080',label='Ookla Up Speed')
			if abs(max(upspeed)-min(upspeed)) > 20:
				ax5.set_yticks(np.arange(minup -10, maxup +13,4))
			else:
				ax5.set_yticks(np.arange(minup -10, maxup +13,2))
			ax5.set_yticklabels([])
			ax5.tick_params(right="off")	
	
			ax6 = ax1.twinx()								## ADD another plot
			ax6.plot(x, downspeed_st, c='#4B0082',label='Ookla Down Speed')
			if abs(max(downspeed)-min(downspeed)) > 20:
				ax6.set_yticks(np.arange(mindl -20, maxdl +3,4))
			else:
				ax6.set_yticks(np.arange(mindl -20, maxdl +3,2))
			#Turn off numbers
			ax6.set_yticklabels([])
			# turn off ticks
			ax6.tick_params(right="off")
			
			
			h1, l1 = ax1.get_legend_handles_labels()
			h2, l2 = ax2.get_legend_handles_labels()
			h3, l3 = ax3.get_legend_handles_labels()
			h4, l4 = ax4.get_legend_handles_labels()
			h5, l5 = ax5.get_legend_handles_labels()
			h6, l6 = ax6.get_legend_handles_labels()

			plt.legend(h1+h6+h2+h5+h3+h4, l1+l6+l2+l5+l3+l4, loc=1)
			# zorder sets paint level in front of plots
			fig.tight_layout()
			plt.savefig('speed.png')	# save the figure to file
			plt.close()
			print ("Plot Complete...\nDownload: {} Mbps\nUpload: {} Mbps\nPing: {}s\nTime: {}"\
			.format(download_now,upload_now,ping_now,str(time.strftime("%d-%m-%Y"))))
			print ("Waiting an hour before testing again.")
			time.sleep(3600)
		

		
		except KeyboardInterrupt:
			print('Interrupted by keyboard')
			driver.quit()
			display.stop()
			print "Stopping driver"
			sys.exit(0)
			
		except:
			driver.quit()
			display.stop()
			print ("Unexpected error:", sys.exc_info()[0])
			continue

if __name__ == "__main__":
    main()
