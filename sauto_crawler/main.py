import sautoParser
import crawler
import os
import csv
import time

testUrl="https://www.sauto.cz/osobni/detail/ford/mondeo/18753802"

# How many ms to wait before calling next request
politenessTime=0.5

# Base address
sautoBaseAddress="http://www.sauto.cz"

def initResultFile(fileName):
	"""
	Initialize file to store extracted data in. Check that it
	eixst or create it and add csv header.  
	"""
	if not os.path.isfile(fileName):
		with open(fileName, "w+") as file:
			writer = csv.writer(file)
			writer.writerow(sautoParser.getDataHeaders())

def processSearchResultPage(pageNum, browser):
	"""
	Download and process one page of search results. Returns list
	of extracted data about all cars in the given page.
	"""
	print("Processing search result page %s" % str(pageNum))
	searchPage = crawler.downloadSearchListPage(page=pageNum, browser = browser)
	adLinks = sautoParser.parseSearchListPage(searchPage)
	data = []
	for adLink in adLinks:
		print("Downloading ad %s" % adLink)
		link = sautoBaseAddress + adLink
		content = crawler.downloadPage(link)

		print("Parsing ad %s" % adLink)
		autoData = sautoParser.parseAdPage(content)
		autoData.append(adLink)
		data.append(autoData)

		print("Polite wait...")
		time.sleep(politenessTime)
	
	print("Done, ads extraced: %s" % str(len(data)))
	return data


def saveDataToFile(fileName, data):
	with open(fileName, "a") as file:
		writer = csv.writer(file)
		writer.writerows(data)

def main():
	resultFile = "data.csv"
	initResultFile(resultFile)

	print("Initializing browser")
	browser = crawler.createHeadlessBrowser()

	for page in range(1,600):
		data = processSearchResultPage(page, browser)
		saveDataToFile(resultFile, data)

	
	# searchPage = ""
	# with open("crawled/search-1.html", "r") as file:
	# 	searchPage = file.read()
	
	# if len(searchPage) == 0:
	# 	browser = crawler.createHeadlessBrowser()
	# 	searchPage = crawler.downloadSearchListPage(page=1, browser = browser)
	# 	with open('crawled/search-1.html', 'w') as file:
	# 		file.write(searchPage)
	# adLinks = sautoParser.parseSearchListPage(searchPage)
	# print(adLinks)
	
	# with open('crawled/test.html', 'w') as file:
	# 	file.write(content)
		
main()