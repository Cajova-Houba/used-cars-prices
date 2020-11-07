import requests
from selenium import webdriver
from datetime import datetime
import os
import shutil
from bs4 import BeautifulSoup
import time
import re

"""
Crawler for used cars on www.sauto.cz.

Downloads 665 pages of search results to folder crawled where it creates following structure:

 + crawled
	+ {timestamp}
		- page-1.html
		+ page-1
			- ad1.html
			- ad2.html
			...
"""

# The output folder's name is the current date
outputFolderNamePattern="%Y-%m-%d"

#
#10k results with the 1st page having 25 and others 15.
#25 + 665*15 = 10000
#By iterating over 665 pages we lose the last 15 results but who cares.
#
maxPage=3
outFolderName="../crawled"

# How many ms to wait before calling next request
politenessTime=0.5

# Base address
sautoBaseAddress="http://www.sauto.cz"

baseSearchUrl="https://www.sauto.cz/osobni/hledani#!category=1&condition=1&condition=2&condition=4&priceMax=%s&tachometrMax=%s&yearMin=%s&page=%s"

def crawl():
	print("initializing output folder")
	outDirName = initOutputFolder()

	print("Initializing browser")
	browser = createHeadlessBrowser()

	for page in range(1,maxPage):
		processSearchResultPage(page, browser, outDirName)
		politeWait()

def initOutputFolder():
	"""
	Checks whether the output folder outFoldername_{timstamp} exists and creates it if not. If the
	folder already exists, it will be deleted.
	Name is returned.
	"""
	timestampSuffix = datetime.now().strftime(outputFolderNamePattern)
	folderName = outFolderName + "/" + timestampSuffix
	if os.path.exists(folderName):
		shutil.rmtree(folderName)
	
	os.makedirs(folderName)
	return folderName


def processSearchResultPage(pageNum, browser, outDirName):
	"""Download and process one page of search results and save it to file.

	Args:
		pageNum ([number]): Number of the search page to download.
		browser ([type]): Instance of browser to be used.
		outDirName ([type]): Name of the folder to store downloaded page to.
	"""
	print("Processing search result page %s" % str(pageNum))
	searchPage = downloadSearchListPage(page=pageNum, browser = browser)
	pageName = "page"+str(pageNum)
	savePageToFile(searchPage, outDirName+"/"+pageName+".html")
	print("Search result page downloaded")

	pageDir = outDirName+"/"+pageName
	os.makedirs(pageDir)
	downloadAdsFromSearchResultPage(searchPage, pageDir, browser)

	print("Done")

def downloadAdsFromSearchResultPage(pageContents, pageDir, browser):
	"""Parses ad links from search result page, downloads them and saves 
	all of them to pageDir.

	Args:
		pageContents (string): HTML contents of the search results page.
		pageDir (string): Relative path to the directory where downloaded pages are to be stored.
		browser ([type]): Instance of browser to be used.
	"""
	links = parseSearchListPage(pageContents)
	cntr = 1
	for adLink in links:
		print("Downloading ad "+str(cntr))
		content = downloadPage(sautoBaseAddress + adLink)
		print("Saving ad "+str(cntr))
		savePageToFile(content, pageDir+"/ad"+str(cntr)+".html")
		cntr = cntr + 1
		print("Done")
		politeWait()

def downloadPage(url):
	"""
	Use requests library to download given 
	HTML page and return its' content.
	"""
	r = requests.get(url)
	return r.text

def savePageToFile(pageContent, outFileName):
	"""Stored html page into given file.

	Args:
		pageContent (string): HTML content of the page.
		outFileName (string): File t store the page to.
	"""
	with open(outFileName, "wb+") as file:
		file.write(pageContent.encode("utf8"))

def downloadSearchListPage(page, browser, priceMax=100000, tachometrMax=200000, yearMin=2000):
	"""
	Downloads the content of one search list page. Because the search list is fetched by JS, the
	Selenium library is used to get it.
	"""
	url = baseSearchUrl % (priceMax, tachometrMax, yearMin, page)
	
	browser.get(url)
	return browser.page_source

def parseSearchListPage(pageContent):
	"""
	Use BeautifulSoup library to parse the HTML
	content of one search list page and return 
	list of links to ads.
	"""
	soup = BeautifulSoup(pageContent, 'html.parser')
	adLinks = []
	
	items = soup.find_all("div", id=re.compile("^item_\d{8}"))
	for item in items:
		itemLink = item.a['href']
		if not isItemAdvertisement(itemLink):
			adLinks.append(itemLink)
	
	return adLinks

def isItemAdvertisement(itemLink):
	"""
	Check if the item is paid advertisement by its link and return
	true if it is. Links to paid items end with 'goFrom=po'.
	"""
	return itemLink.endswith('goFrom=po')
	
def createHeadlessBrowser():
	"""
	Create and return instance of a Selenium headless browser.
	"""
	fireFoxOptions = webdriver.FirefoxOptions()
	fireFoxOptions.headless = True
	return webdriver.Firefox(options=fireFoxOptions)

def politeWait():
	print("Polite wait...")
	time.sleep(politenessTime)

def main():
	print("Crawlin' baby!")
	crawl()

main()
	