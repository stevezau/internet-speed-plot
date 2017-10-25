# NBN Speed
There has been alot of talk around the NBN speeds in Australia lately, so I thought that I would put my two cents
in for anyone who wants some data to complain with. 

This python script will grap your IP address and get the JSON data from http://ipinfo.io/ , which includes your ISP data for the plot information, it also uses the speed-test python API to get the up, down and ping results of your internet connection hourly.

Every hour it will use matplotlib to create a plot of your current connection speeds and save them to a image file, every 24 hours it will make a copy of your daily plot and save it in the same directory for you to check or send off to complain.

This was created in python 2.7 but tested with Python 3.6 also and seems to work fine.


## Prerequisites

You will require the following for this to run:

Python 2.x or 3.x

speedtest-cli

matplotlib

numpy

## Install & Run on Linux
```
sudo apt-get install python-setuptools python-dev build-essential 
sudo easy_install pip 
pip install speedtest-cli requests matplotlib numpy requests
git clone https://github.com/brentoncollins/nbnspeed

python nbnspeed.py
```
## Install & Run on Windows
You will need to install Python 2.x or 3.x https://www.python.org/downloads/windows/

Ensure when you install python, on the first install page click add to PATH, this will allow you to run python from CMD with no worries.

You will need to install Microsoft Visual C++ in order to install the python packages which ate required, you can find this here
http://landinghub.visualstudio.com/visual-cpp-build-tools. (takes a while to install, which is kind of annoying :( sorry)

Install git from https://git-scm.com/download/win

With these installed you should be able to clone the files to a directory and run the setup.

Open CMD from the start menu then.
```
git clone https://github.com/brentoncollins/nbnspeed
pip install --user numpy scipy matplotlib speedtest-cli requests
python nbnspeed.py
```
## Optimised usage
The speed-test package will try and locate the nearest test server to you, which works most of the time. If you hare having trouble with your speeds and think that they could be better you can browse to https://www.speedtestserver.com/ and find the closest server to you.

Find in nbnspeed.py where it says:
```
servers = []
```
and change it to the server number which you located on the website above and save the changes.
```
servers = [2627]
```
e.g. 2627 points to Telstra in Perth city, which is the closest server to me.

## Feedback

If you have anyfeedback, or it doesnt work, please message me as this is the first commit and I most probably have forgotten something.
I have tested it on Python 2.x and 3.x on windows and linux.
brenton.collins@outlook.com
