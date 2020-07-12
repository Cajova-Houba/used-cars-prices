import requests
from selenium import webdriver

"""
Crawler for used cars on www.sauto.cz.
"""

baseSearchUrl="https://www.sauto.cz/osobni/hledani#!category=1&condition=1&condition=2&condition=4&priceMax=%s&tachometrMax=%s&yearMin=%s&page=%s"

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
	
	