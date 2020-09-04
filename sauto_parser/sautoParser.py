from bs4 import BeautifulSoup
import re

"""
Parser for data crawled from sauto.cz
"""

def getDataHeaders():
	"""
	Return data headers for csv files.
	"""
	return ["brand", "model", "price", "year", "kilometers", "power", "link"]

def getEmptyDataRow():
	"""
	Return empty data structure for extracted data.
	Link is to be appended elsewhere.
	"""
	return ["", "", 0, 0, 0, 0]

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
	extractedData = getEmptyDataRow()
	
	res = soup.find_all(attrs={"data-sticky-header-value-src":"brandAndModel"})
	if (len(res) > 0):
		extractedData[0]=res[0].contents[1].text.strip()
		extractedData[1]=res[0].contents[3].text.strip()
		
	res = soup.find(id="finalPrice")
	if (len(res) > 0):
		extractedData[2]=res.span.strong.text.strip().replace("\xa0","")
		
	res = soup.find_all(attrs={"data-sticky-header-value-src":"year"})
	if (len(res) > 0):
		extractedData[3]=res[0].text.strip()
	
	kms = extractValueFromParamTableHead(soup, "Tachometr:")
	if (kms is not None):
		extractedData[4]=kms
		
	power = extractValueFromParamTableHead(soup, "Výkon:")
	if (power is not None):
		extractedData[5]=power
	
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
	
	