from bs4 import BeautifulSoup
import re
import os
import shutil
import csv

"""
Parser for data crawled from sauto.cz
"""

# delimiter for the output csv
outputDelimiter=","

def parse(inputFolder):
	"""Goes through the folder structure created by crawler and parses ad pages.

	Args:
		inputFolder (string): Input folder which should point to the folder with search and ad pages. E.g. crawled/{timestamp}
	"""
	print("Initializing output file")
	initResultFile("data.csv")
	processResultPages(inputFolder, "data.csv")


def initResultFile(fileName):
	"""
	Initialize file to store extracted data in. Check that it
	eixst or create it and add csv header.  
	"""
	if not os.path.isfile(fileName):
		data = []
		data.append(getDataHeaders())
		saveDataToFile(fileName, data)

def processResultPages(inDirName, outFileName):
	print("Processing input folder: "+inDirName)
	files = os.listdir(inDirName)
	for f in files:
		if not os.path.isfile(inDirName+"/"+f):
			processResultPageFolder(inDirName+"/"+f, outFileName)
	
def processResultPageFolder(folderName, outFileName):
	print("Processing folder "+folderName)
	files = os.listdir(folderName)
	data = []
	for f in files:
		if f.endswith(".html") and os.path.isfile(folderName+"/"+f):
			print("Parsing page "+f)
			with(open(folderName+"/"+f, "rb")) as adPage:
				htmlContent = adPage.read().decode()
			data.append(parseAdPage(htmlContent))
	
	print("Saving parsed data")
	saveDataToFile(outFileName, data)
	print("Done")

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

def saveDataToFile(fileName, data):
	"""Saves multiple lines to csv file.

	Args:
		fileName (string): Name of the outputfile to append data to.
		data (array[][]): Array of array of data items (array of rows to save).
	"""
	with open(fileName, "ab") as file:
		for dataLine in data:
			lineStr = ""
			for dataItem in dataLine:
				lineStr = lineStr + dataItem + outputDelimiter
			file.write((lineStr[:-1] + "\n").encode("utf8"))

def main():
	print("Parsin' baby!")
	parse("../crawled/2020-09-04_18-27-42")

main()