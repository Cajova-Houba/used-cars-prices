import requests
from selenium import webdriver
from datetime import datetime
import os
import shutil

"""
Crawler for used cars on www.sauto.cz.

Downloads 665 pages of search results to folder crawled_{timestamp}.
"""

"""
10k results with the 1st page having 25 and others 15.
25 + 665*15 = 10000
By iterating over 665 pages we lose the last 15 results but who cares.
"""
maxPage=2
outFolderName="crawled"

baseSearchUrl="https://www.sauto.cz/osobni/hledani#!category=1&condition=1&condition=2&condition=4&priceMax=%s&tachometrMax=%s&yearMin=%s&page=%s"

def crawl():
	print("initializing output folder")
	outDirName = initOutputFolder()

	print("Initializing browser")
	browser = createHeadlessBrowser()

	for page in range(1,maxPage):
		processSearchResultPage(page, browser, outDirName)

def initOutputFolder():
	"""
	Checks whether the output folder outFoldername_{timstamp} exists and creates it if not. If the
	folder already exists, it will be deleted.
	Name is returned.
	"""
	timestampSuffix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	folderName = outFolderName + "_" + timestampSuffix
	if os.path.exists(folderName):
		shutil.rmtree(folderName)
	
	os.makedirs(folderName)
	return folderName


def processSearchResultPage(pageNum, browser, outDirName):
	"""Download and process one page of search results and save it to file.

	Args:
		pageNum ([number]): Number of the search page to download
		browser ([type]): Instance of browser to be used
		outDirName ([type]): Name of the folder to store downloaded page to.
	"""
	print("Processing search result page %s" % str(pageNum))
	searchPage = downloadSearchListPage(page=pageNum, browser = browser)
	with open(outDirName+"/page-"+str(pageNum)+".html", "wb") as file:
		file.write(searchPage.encode("utf8"))
	print("Done")

def downloadPage(url):
	"""
	Use requests library to download given 
	HTML page and return its' content.
	"""
	r = requests.get(url)
	return r.text
	

def downloadSearchListPage(page, browser, priceMax=100000, tachometrMax=200000, yearMin=2000):
	"""
	Downloads the content of one search list page. Because the search list is fetched by JS, the
	Selenium library is used to get it.
	"""
	url = baseSearchUrl % (priceMax, tachometrMax, yearMin, page)
	
	browser.get(url)
	return browser.page_source
	
def createHeadlessBrowser():
	"""
	Create and return instance of a Selenium headless browser.
	"""
	fireFoxOptions = webdriver.FirefoxOptions()
	fireFoxOptions.headless = True
	return webdriver.Firefox(options=fireFoxOptions)

def main():
	print("Crawlin' baby!")
	crawl()

main()
	