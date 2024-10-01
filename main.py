import requests
import csv
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup

def getRegistered():
	url = 'https://www.logickaolympiada.cz/'
	response = requests.get(url)

	if response.status_code != 200:
		logError(f"status code {response.status_code}")
		return False


	# find the correct tag
	soup = BeautifulSoup(response.text, 'html.parser')
	span_tag = soup.find('span', string="Počet registrovaných soutěžících:   ")
	parent_tag = span_tag.parent
	sibling_tag = parent_tag.find_next_sibling('strong')

	number = sibling_tag.get_text(strip=True).split()[0]
	return number
	sleeptime = (60 - now.minute) * 60 - now.second

def getSolving():
	url = 'https://www.logickaolympiada.cz/'
	response = requests.get(url)

	if response.status_code != 200:
		logError(f"status code {response.status_code}")
		return False

	# find the correct tag
	soup = BeautifulSoup(response.text, 'html.parser')
	tag = soup.find(string=re.compile(r"V tuto chvíli test řeší.*soutěžících"))
	number = re.search(r'\d+', tag).group()

	return number

def logCsv(columns):
    with open("data-solving.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)


while True:
	# wait for the next hour
	now = datetime.now()
	sleeptime = (60 - now.minute) * 60 - now.second
	print(f"Sleeping {sleeptime} seconds.")
	time.sleep(sleeptime)

	now = datetime.now()
	
	# scrape
	result = getSolving()

	# print and log
	print(f"It is {now.strftime('%Y-%m-%d %H:%M')} and {result} people are currently solving the test.")
	logCsv([
		now.strftime("%Y-%m-%d %H:%M"),
		result
	])