import requests
from bs4 import BeautifulSoup
import re

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

def parseSearchListPage(pageContent):
	"""
	Use BeautifulSoup library to parse the HTML
	content of one search list page and return 
	list of links to ads.
	"""
	soup = BeautifulSoup(pageContent, 'html.parser')
	adLinks = []
	
	#resElement = soup.find_all("div", id=re.compile("^item_\d{8}"))
	resElement = soup.find("div", id="changingResults")
	print(resElement)
	if (resElement is not None):
		items = resElement.find_all("div")
		print(items)
		for item in items:
			print(item.a.href)
	
	return adLinks
	

def downloadSearchListPage(page,priceMax=100000, tachometrMax=200000, yearMin=2000):
	"""
	Downloads the content of one search list page.
	"""
	url = baseSearchUrl % (priceMax, tachometrMax, yearMin, page)
	print(url)
	return downloadPage(baseSearchUrl)
	
def main():
	#content = downloadPage(testUrl)
	#extractedData = parseAdPage(content)
	#print(extractedData)
	
	searchPage = downloadSearchListPage(page=1)
	parseSearchListPage(searchPage)
	
	# with open('crawled/test.html', 'w') as file:
	# 	file.write(content)
		
main()
	
	