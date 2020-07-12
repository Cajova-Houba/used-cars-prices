import sautoParser
import crawler
import os
import csv

testUrl="https://www.sauto.cz/osobni/detail/ford/mondeo/18753802"

# How many ms to wait before calling next request
politenessTime=800

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
	searchPage = crawler.downloadSearchListPage(page=1, browser = browser)
	adLinks = sautoParser.parseSearchListPage(searchPage)

def main():
	initResultFile("data.csv")
	return

	content = crawler.downloadPage(testUrl)
	extractedData = sautoParser.parseAdPage(content)
	#print(extractedData)
	
	searchPage = ""
	with open("crawled/search-1.html", "r") as file:
		searchPage = file.read()
	
	if len(searchPage) == 0:
		browser = crawler.createHeadlessBrowser()
		searchPage = crawler.downloadSearchListPage(page=1, browser = browser)
		with open('crawled/search-1.html', 'w') as file:
			file.write(searchPage)
	adLinks = sautoParser.parseSearchListPage(searchPage)
	print(adLinks)
	
	# with open('crawled/test.html', 'w') as file:
	# 	file.write(content)
		
main()