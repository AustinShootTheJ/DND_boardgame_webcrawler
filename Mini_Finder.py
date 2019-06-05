from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import Request
import re
import requests
#workbook imports
import openpyxl
from openpyxl import Workbook
import os
import csv


#url of the site to be scraped
#wrath of ashardalon
urls = ['https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1311.R3.TR6.TRC1.A0.H0.Xwrath+of+ash.TRS0&_nkw=wrath+of+ashardalon+board+game&_sacat=0',
'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312.R1.TR0.TRC2.A0.H1.X.TRS5&_nkw=the+legend+of+drizzt+board+game&_sacat=0',
'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR11.TRC2.A0.H0.Xtemple+of.TRS1&_nkw=temple+of+elemental+evil+board+game&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=the+legend+of+drizzt+board+game',
'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1312.R1.TR11.TRC2.A0.H0.Xwa.TRS1&_nkw=waterdeep+dungeon+of+the+mad+mage+board+game&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=temple+of+elemental+evil+board+game&LH_TitleDesc=0',
'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=assult+of+the+giants+boardgame&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=waterdeep+dungeon+of+the+mad+mage+board+game&LH_TitleDesc=0']
ebay_items_dict = {}
for url in urls:


	#opens a url session, copies down the page and closes the session.
	uClient = uReq(url)
	page_html = uClient.read()
	uClient.close()

	#parses the page using bs4
	page_soup = soup(page_html,"html.parser")

	#dictionary to store best selling amazon items
	temp_items_dict = {}

	#stores all items on the best seller page
	items = page_soup.findAll("li", {"class": "s-item"})



	for item in items:

		try:
			title = item.find("h3", {"class": "s-item__title"}).text.strip()
		except:
			#print("No title listed")
			continue
	
		try:
			raw_price = item.find("span", {"class": "s-item__price"}).text.strip()
			format_price = re.findall(r'[\d,]+\.\d\d',raw_price)
			joined_price = ''.join(format_price)
			price = joined_price.replace(',','')
			final_price = (float(price))

		except:
			#print("No price listed")
			continue

		try:
			shipping = item.find("span", {"class": "s-item__shipping s-item__logisticsCost"}).text.strip()
		except:
			#print("No shipping listed")
			continue

		try:
			link = item.find("a", {"class": "s-item__link"})
			item_link = link["href"]
		except:
			#print("No link listed")
			continue
		if (final_price > 10.00 and final_price < 40.00 ):
			temp_items_dict[title] = [final_price,shipping,item_link]


	ebay_items_dict.update(temp_items_dict.items())

	


w = csv.writer(open("boardgamePrices.csv","w"))
for key, [val1,val2,val3] in ebay_items_dict.items():
	w.writerow([key,val1,val2,val3])

