#!/usr/bin/env python
from bs4 import BeautifulSoup
import unittest
from selenium import webdriver
import platform
system = platform.system().lower()
if system != "windows":
	from pyvirtualdisplay import Display
	display = Display(visible=0, size=(800, 600))
	display.start()
import sys
import traceback
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
import shutil
import os

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
global driver
driver = webdriver.Firefox()
class scrape:
# Scrape the Ookala web page for results, after running the speed test in selenium.

	def __init__(self):
		print("Ookala webscrape....")
		print("Opening webdriver....")
		driver.get('http://beta.speedtest.net/')
		driver.find_element_by_xpath(".//*[@id='container']/div[2]/div/div/div/div[3]/div[1]/div[1]/a/span[3]").click()
		print("Testing Down Speed...\n")
		time.sleep(25)
		print("Testing Up Speed...\n")
		time.sleep(25)
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
def option_type():
#  Choose an option to either run the API, web-scrape the data or both options.
	while True:
		try:
			option = int(input("Enter an option.\n\
					1. Speedtest API\n\
					2. Ookala webscrape\n\
					3. Combination of both.\n\n"))
		except NameError:
			print("Sorry, Please enter either 1, 2 or 3.")
			continue
		if option == 1 or 2 or 3:
			return option
			break
		
def main():
# Crammed everything into the main function......
	option = option_type()

# If only using either the API or web-scrape use these lists
	if option == 1 or option == 2:
		downspeed=[]
		upspeed=[]
		ping_time=[]
# If web-scrape and API, set these 6 lists for use.
	if option == 3:
	
		upspeed_st=[]
		ping_time_st=[]
		downspeed_st = []
	
		downspeed=[]
		upspeed=[]
		ping_time=[]
	
	time_now =[]
	counter = 0
	
	while True:
		try:
			
			if option == 2 or option == 3:
				speettest = scrape()
				
			# Run the web-scrape if web-scrape only or both options.
			
			counter += 1
			if counter == 25:
				timestr = str(time.strftime("%d-%m-%Y"))
				shutil.copy("speed.png", timestr + ".png")
				counter = 0
				
			# If the length of the list of time values is more then 25, make a copy of the plot image,
			# then set the counter to 0 to wait for another 24 hours of testing before copying again.
				
			if option == 1 or option == 3:
				
				# Run the API if single or both.
	
				print("Speedtest API running....")
				print("Please Wait....")
				servers =[]
				# If you want to test against a specific server visit https://www.speedtestserver.com/
				# and find a server you want to test with e.g. servers = [2627] which is Perth
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
				# Append the values to the lists.
				
			time_now.append(time.strftime("%I %p"))
			# Append the current hour to the time_now list.
			
			if option == 3:
				downspeed_st.append(float(speettest.down))
				upspeed_st.append(float(speettest.up))
				ping_time_st.append(float(speettest.ping))
				# Append the values to the lists if both.
			if option == 2:
				downspeed.append(float(speettest.down))
				upspeed.append(float(speettest.up))
				ping_time.append(float(speettest.ping))
				# Apend the values to the list if web-scrape
			if len(time_now) >= 25:
				del downspeed[0],downspeed_st[0],upspeed[0],upspeed_st[0],ping_time[0],ping_time_st[0],time_now[0]
				# If it has run for a whole 24 hours, remove the first value in all of the lists 
				# to keep the x axis at 24.
				# This is becasue we only want a plot image with 24 x-axis points for a whole day.
			if option == 3:	
				maxdl = round(max(downspeed+downspeed_st))
				mindl = round(min(downspeed+downspeed_st))
				maxup = round(max(upspeed+upspeed_st))
				minup = round(min(upspeed+upspeed_st))
				maxping = round(max(ping_time+ping_time_st))
				minping = round(max(ping_time+ping_time_st))
				# If web-scrape & API add both of the lists together, 
				# find the maximum number after the lists have been added together
				# then round to a whole number, this is to ensure the y values of the plot are kept at whole number.
			if option == 1 or option == 2:
				maxdl = round(max(downspeed))
				mindl = round(min(downspeed))
				maxup = round(max(upspeed))
				minup = round(min(upspeed))
				maxping = round(max(ping_time))
				minping = round(max(ping_time))
				# Same as above but only using the lists that are used if it a single test.
					
			# Start of the plotting.	
			x = np.arange(1,len(time_now)+1)								
			# Set the x axis points.
			fig, ax1 = plt.subplots()
			plt.grid()
			#Choose the plot type
			ax1.plot(x, downspeed, c='#FF6347', label='Down speed API')		
			# Draw the first plot line for the Down Speed API
			if option == 3:
				ax1.set_xlabel("{} - {} - {}\nOokla - MAX\MIN - Down {}\{} - Up {}\{} - Ping {}\{} ms\nAPI MAX\MIN\
				- Down {}\{} - Up {}\{} - Ping {}\{} ms"\
				.format(str(speettest.isp),str(speettest.city),str(time.strftime("%d-%m-%Y")),\
				max(downspeed_st),min(downspeed_st),max(upspeed_st),min(upspeed_st),max(ping_time_st),min(ping_time_st)\
				,max(downspeed),min(downspeed),max(upspeed),min(upspeed),max(ping_time),min(ping_time)))
			if option == 2:
				ax1.set_xlabel("{} - {} - {}\nOokla - MAX\MIN - Down {}\{} - Up {}\{} - Ping {}\{} ms\n"\
				.format(str(speettest.isp),str(speettest.city),str(time.strftime("%d-%m-%Y")),\
				max(downspeed),min(downspeed),max(upspeed),min(upspeed),max(ping_time),min(ping_time)))
				
			if option == 1:
				ax1.set_xlabel("{} - {}\API - MAX\MIN - Down {}\{} - Up {}\{} - Ping {}\{} ms\n"\
				.format(results_dict['server']['name'],str(time.strftime("%d-%m-%Y")),\
				max(downspeed),min(downspeed),max(upspeed),min(upspeed),max(ping_time),min(ping_time)))
			# Due to the three options I needed to change the x-axis label to suit.	
				
			ax1.set_ylabel('Down Speed', color='#FF6347')
			# Set the Y label and color
			ax1.tick_params('y', colors='#FF6347')	
			if abs(max(downspeed)-min(downspeed)) > 20:
				ax1.set_yticks(np.arange(mindl -20, maxdl +3,4))
			else:
				ax1.set_yticks(np.arange(mindl -20, maxdl +3,2))
			# If the range between maximum and minimum download speeds is < 20 I keep the Y poins of mutiples of 2
			# if > 20 step the y axis by 4 this stops all the numbers cramming up along the spine.
			
			ax1.set_xticklabels( time_now, rotation=45 )
			plt.xticks(x,time_now)								
			# Set the x labels rotation and values.
			
			
			ax2 = ax1.twinx()						## ADD another plot and same as above
			ax2.plot(x, upspeed, label='Up Speed API')
			ax2.set_ylabel('Up Speed', color='b')
			ax2.tick_params('y', colors='b')
			if abs(max(upspeed)-min(upspeed)) > 20:
				ax2.set_yticks(np.arange(minup -10, maxup +13,4))
			else:
				ax2.set_yticks(np.arange(minup -10, maxup +13,2))

			ax3 = ax1.twinx()						## ADD another plot and same as above
			ax3.plot(x, ping_time, c = '#006400', linestyle=':',label='Ping API')
			ax3.set_ylabel('Ping', color='#006400')
			ax3.tick_params('y', colors='#006400')
			ax3.set_yticks(np.arange(0, maxping +150,10))
			ax3.spines['right'].set_position(('axes', 1.15))
			
			h1, l1 = ax1.get_legend_handles_labels()
			h2, l2 = ax2.get_legend_handles_labels()
			h3, l3 = ax3.get_legend_handles_labels()
			# Set the legend labels.
			
			if option == 1 or option == 2:
				plt.legend(h1+h2+h3, l1+l2+l3, loc=1)
			# Setup the legend
			
			if option == 3:
			
			# If I am using option 3 for both which will include 6 plots instead of just 3, add the next 3.
				ax4 = ax1.twinx()					## ADD another plot and same as above
				ax4.plot(x, ping_time_st, c = '#000000', linestyle=':',label='Ookla Ping')
				ax4.set_yticks(np.arange(0, maxping +150,10))
				
				ax4.set_yticklabels([])
				ax4.tick_params(right="off")
				# Due to not needing duplicate spines for the two duplicate plots, I am refering to the same spines
				# and turning the last three off, I only need one download, one upload and one ping spine.
				
				ax5 = ax1.twinx()					## ADD another plot and same as above
				ax5.plot(x, upspeed_st, c = '#000080',label='Ookla Up Speed')
				if abs(max(upspeed)-min(upspeed)) > 20:
					ax5.set_yticks(np.arange(minup -10, maxup +13,4))
				else:
					ax5.set_yticks(np.arange(minup -10, maxup +13,2))
				ax5.set_yticklabels([])
				ax5.tick_params(right="off")	
				# As above
				
				ax6 = ax1.twinx()					## ADD another plot and same as above
				ax6.plot(x, downspeed_st, c='#4B0082',label='Ookla Down Speed')
				if abs(max(downspeed)-min(downspeed)) > 20:
					ax6.set_yticks(np.arange(mindl -20, maxdl +3,4))
				else:
					ax6.set_yticks(np.arange(mindl -20, maxdl +3,2))
				#Turn off numbers
				ax6.set_yticklabels([])
				# turn off ticks
				ax6.tick_params(right="off")
				
				h4, l4 = ax4.get_legend_handles_labels()
				h5, l5 = ax5.get_legend_handles_labels()
				h6, l6 = ax6.get_legend_handles_labels()
				# As above added more due to using both options.
				plt.legend(h1+h6+h2+h5+h3+h4, l1+l6+l2+l5+l3+l4, loc=1)
				# As above 
				
			fig.tight_layout()
			plt.savefig('speed.png')	# save the figure to file
			plt.close()
			print ("Plot Complete...\nDownload: {} Mbps\nUpload: {} Mbps\nPing: {}s\nTime: {}"\
			.format(str(downspeed[-1]),str(upspeed[-1]),str(ping_time[-1]),str(time.strftime("%I %p"))))
			print ("Waiting an hour before testing again.\n")
			time.sleep(3600)
		

		
		except KeyboardInterrupt:


			driver.quit()
			display.stop()
			print ("Stopping driver")
			sys.exit(0)
		except Exception:
			print(traceback.format_exc())
			print(sys.exc_info()[0])		

			continue

if __name__ == "__main__":
    main()
