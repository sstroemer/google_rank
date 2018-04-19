#!/usr/bin/python
import sys
import urllib
import datetime
import time

from urllib import request, parse


def main():
	domains = readDomains()
	keywords = readKeywords()

	for keyword in keywords:
		print('-----------------------------------------')
		print('Checking "' + keyword + '"')
		parseResults(search(keyword), keyword, domains)
		print('Delay')
		time.sleep(60)

		
def parseResults(result, keyword, domains):
	start = 0
	rank = 1
	
	while True:
		start = result.find(b'<h3 class="r"><a href', start)
		if start == -1:
			# write result to file (100 means > 100)
			file = open('results\\' + keyword + '.csv', 'a+')
			file.write('%s;%d;%s\n' % (datetime.datetime.now(), 100, domain))
			file.close()
			return

		start += 23
		end   = result.find(b'"', start)

		for domain in domains:
			if result[start:end].find(domain.encode()) != -1:
				# output
				print('Domain ' + domain + ' hit. Rank: ' + str(rank))
				# write result to file
				file = open('results\\' + keyword + '.csv', 'a+')
				file.write('%s;%d;%s\n' % (datetime.datetime.now(), rank, domain))
				file.close()
				return

		rank += 1	


def readKeywords():
	file = open("keywords.txt", "r")
	lines = file.readlines()
	file.close()

	lines = list(map(str.strip, lines))
	return lines
	
	
def readDomains():
	file = open("domains.txt", "r")
	lines = file.readlines()
	file.close()

	lines = list(map(str.strip, lines))
	return lines	

	
def getHTML(url):
	req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36' })
	return urllib.request.urlopen(req).read()

	
def search(keyword):
	return getHTML("http://www.google.at/search?num=100&q=" + urllib.parse.quote_plus(keyword))

	
if __name__ == "__main__":
    main()
