# Project Title
There has been alot of talk around the NBN speeds in Australia lately, so I thought that I would put my two cents
in for anyone who wants some data to complain with, this python script will grap your IP address and get the JSON data from
http://ipinfo.io/ which includes your ISP data for the plot information, it also uses the speed-test python API 
to get the up, down and ping results of your internet connection hourly.
Every hour it will use matplotlib to create a plot of your current connection speeds and save them to a image file,
every 24 hours it will make a copy of your daily plot and save it in the same directory for you to check or send off to complain.
This was created in python 2.7

## Prerequisites

You will require the following for this to run:
```
sudo apt-get install python-setuptools python-dev build-essential 
sudo easy_install pip 

pip install speedtest-cli
pip install matplotlib
pip install numpy

```

## Running the script
With these installed you should be able to run:
```
sudo python nbnspeed.py

```


## Feedback

If you have anyfeedback, or it doesnt work, please message me as this is the first commit and I most probably have forgotten something.
brenton.collins@outlook.com
