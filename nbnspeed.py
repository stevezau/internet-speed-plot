#!/usr/bin/env python

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

r = requests.get('http://ipinfo.io/json')
r.raise_for_status()
data = json.loads(r.content.decode('utf-8'))
IP=data['ip']
org=data['org']
city = data['city']
country=data['country']
region=data['region']

print('Your IP detail\n ')
print('IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0}'.format(org,region,country,city,IP))

def main():
	ping_time=[]
	up=[]
	time_now =[]
	dl=[]
	counter = 0
	while True:
		counter += 1
		if counter == 25:
			timestr = str(time.strftime("%d-%m-%Y"))
			shutil.copy("speed.png", timestr + ".png")
			counter = 0
			
		#check_ping()
		# If you want to test against a specific server visit https://www.speedtestserver.com/
		# and find a server you want to test with e.g. servers = [2627] which is Perth
		servers = []

		s = speedtest.Speedtest()
		s.get_servers(servers)
		s.get_best_server()
		s.download()
		s.upload()

		results_dict = s.results.dict()

		download_now = float(round(results_dict['download']/1000000,2))
		upload_now = float(round(results_dict['upload']/1000000,2))
		ping_now = float(round(results_dict['ping'],2))
		
		dl.append(download_now)
		up.append(upload_now)
		ping_time.append(ping_now)
		time_now.append(time.strftime("%I %p"))
		
		if len(dl) >= 25:
			del dl[0]
			del up[0]
			del ping_time[0]
			del time_now[0]

		downspeed = dl
		upspeed = up
		ping = ping_time
		now = time_now

		x = np.arange(1,len(now)+1)								
		fig, ax1 = plt.subplots()
		plt.grid()							
		ax1.plot(x, downspeed, c='#FF6347', label='Down speed')		
		ax1.set_xlabel(org + " - " + city)	
		ax1.set_ylabel('Down Speed', color='#FF6347')	
		ax1.tick_params('y', colors='#FF6347')	
		if abs(max(downspeed)-min(downspeed)) > 20:
			ax1.set_yticks(np.arange(round(min(downspeed))-10, round(max(downspeed)+3),2))	
		else:
			ax1.set_yticks(np.arange(round(min(downspeed))-10, round(max(downspeed)+3),1))
		ax1.set_xticklabels( now, rotation=45 )		
		plt.xticks(x,now)								

		ax2 = ax1.twinx()								## ADD another plot
		s2 = np.arange(1,len(now)+1)
		ax2.plot(x, upspeed, label='Up Speed')
		ax2.set_ylabel('Up Speed', color='b')
		ax2.tick_params('y', colors='b')
		if abs(max(upspeed)-min(upspeed)) > 20:
			ax2.set_yticks(np.arange(round(min(upspeed))-5, round(max(upspeed)+8),2))
		else:
			ax2.set_yticks(np.arange(round(min(upspeed))-5, round(max(upspeed)+8),1))

		ax3 = ax1.twinx()								## ADD another plot
		s3 = np.arange(.1,len(now)+1)
		ax3.plot(x, ping, c = '#006400', linestyle=':',label='Ping')
		ax3.set_ylabel('Ping', color='#006400')
		ax3.tick_params('y', colors='#006400')
		nearestping = int(math.ceil((min(ping) / 10.0))) * 10
		ax3.set_yticks(np.arange(0, round(max(ping)+150),10))
		ax3.spines['right'].set_position(('axes', 1.1))

		h1, l1 = ax1.get_legend_handles_labels()
		h2, l2 = ax2.get_legend_handles_labels()
		h3, l3 = ax3.get_legend_handles_labels()

		ax1.legend(h1+h2+h3, l1+l2+l3, loc=1)

		fig.tight_layout()
		plt.savefig('speed.png')	# save the figure to file
		plt.close()
		print ("Plot Complete...\nDownload: {} Mbps\nUpload: {} Mbps\nPing: {}s\nTime: {}"\
		.format(download_now,upload_now,ping_now,str(time.strftime("%d-%m-%Y"))))
		print ("Waiting an hour before testing again.")
		time.sleep(3600)
		
	
if __name__ == "__main__":
    main()
