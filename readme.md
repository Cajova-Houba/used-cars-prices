# Gathering data

Data are gathered by crawling the search results of [sauto](www.sauto.cz).
So far the data I'm interested in are the brand, model, year the car was manufactured, power and kilometers.

Crawler is implemented in python using the [requests](https://requests.readthedocs.io/en/master/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) libraries. The search result page of the sauto.cz is populated
by JS so the [Selenium](https://selenium-python.readthedocs.io/) library (with headless browser) is used for that one.

# Working with the data

As I'm not quite sure what I'm going to want to do with the data I'll just use R to plot them and/or perform some statistical operations over them.
