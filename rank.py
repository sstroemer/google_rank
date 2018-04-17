#!/usr/bin/python
import sys
#import urllib2
import urllib
from urllib.request import urlopen, Request
import urllib.parse

def main(argv):
	if (len(argv) != 2):
		print("Please specify domain name!")
		return 1
	
	domain = argv[1]
	keywords = readKeywords()

	for i in range(0, len(keywords)-1):
		keywords[i] = keywords[i].strip("\n")
		print(keywords[i] + " -> " + str(parseResults(search(keywords[i]), domain)))

def parseResults(result, domain):
	start = 0
	rank = 1
	while (True):
		start = result.find(b'<h3 class="r"><a href', start)
		if (start == -1):
			break

		start += 23
		end   = result.find(b'"', start)

		# print(result[start:end])

		if (result[start:end].find(domain.encode()) != -1):
			# print("Domain hit. Rank: " + rank)
			break

		rank += 1	
	return rank


def readKeywords():
	file = open("keywords.txt", "r")
	lines = file.readlines()
	file.close()
	return lines

def getHTML(url):
	req = Request(url, headers={ 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'})
	return urlopen(req).read()

def search(keyword):
	return getHTML("http://www.google.at/search?num=100&q=" + urllib.parse.quote_plus(keyword))

if __name__ == "__main__":
    main(sys.argv)
