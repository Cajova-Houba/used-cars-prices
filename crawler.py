import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver

"""
Crawler for used cars on www.sauto.cz.
"""

testUrl="https://www.sauto.cz/osobni/detail/ford/mondeo/18753802"

baseSearchUrl="https://www.sauto.cz/osobni/hledani#!category=1&condition=1&condition=2&condition=4&priceMax=%s&tachometrMax=%s&yearMin=%s&page=%s"

def downloadPage(url):
	"""
	Use requests library to download given 
	HTML page and return its' content.
	"""
	r = requests.get(url)
	print(r.url)
	return r.text

def extractValueFromParamTableHead(soup, valueName):
	"""
	Extract value from ad parameter table (located in the thead). 
	The soup object is used to retrieve the table which id is 
	expected to be 'detailParams'.
	
	If the table or the value are not found, None is returned.
	"""
	paramTable = soup.find(id="detailParams")
	if (paramTable is not None):
		rows = paramTable.thead.find_all("tr")
		if (len(rows) > 0):
			for row in rows:
				if (row.th.text == valueName):
					return row.td.text.strip().replace("\xa0","")
					
	# nothing found
	return None

def parseAdPage(pageContent):
	"""
	Use BeautifulSoup library to parse the HTML
	content of an ad page (1 ad = 1 car) and return
	dict with extracted data.
	"""
	soup = BeautifulSoup(pageContent, 'html.parser')
	extractedData = {}
	
	res = soup.find_all(attrs={"data-sticky-header-value-src":"brandAndModel"})
	if (len(res) > 0):
		extractedData["brand"]=res[0].contents[1].text.strip()
		extractedData["model"]=res[0].contents[3].text.strip()
		
	res = soup.find(id="finalPrice")
	if (len(res) > 0):
		extractedData["price"]=res.span.strong.text.strip().replace("\xa0","")
		
	res = soup.find_all(attrs={"data-sticky-header-value-src":"year"})
	if (len(res) > 0):
		extractedData["year"]=res[0].text.strip()
	
	kms = extractValueFromParamTableHead(soup, "Tachometr:")
	if (kms is not None):
		extractedData["kilometers"]=kms
		
	power = extractValueFromParamTableHead(soup, "Výkon:")
	if (power is not None):
		extractedData["power"]=power
	
	return extractedData

def isItemAdvertisement(itemLink):
	"""
	Check if the item is paid advertisement by its link and return
	true if it is. Links to paid items end with 'goFrom=po'.
	"""
	return itemLink.endswith('goFrom=po')

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
	

def downloadSearchListPage(page, browser, priceMax=100000, tachometrMax=200000, yearMin=2000):
	"""
	Downloads the content of one search list page. Because the search list is fetched by JS, the
	Selenium library is used to get it.
	"""
	url = baseSearchUrl % (priceMax, tachometrMax, yearMin, page)
	print(url)
	
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
	#content = downloadPage(testUrl)
	#extractedData = parseAdPage(content)
	#print(extractedData)
	
	searchPage = ""
	with open("crawled/search-1.html", "r") as file:
		searchPage = file.read()
	
	if len(searchPage) == 0:
		browser = createHeadlessBrowser()
		searchPage = downloadSearchListPage(page=1, browser = browser)
		with open('crawled/search-1.html', 'w') as file:
			file.write(searchPage)
	adLinks = parseSearchListPage(searchPage)
	print(adLinks)
	
	# with open('crawled/test.html', 'w') as file:
	# 	file.write(content)
		
main()
	
	