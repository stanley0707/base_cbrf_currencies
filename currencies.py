import urllib.request
from xml.dom import minidom

CB_URL = "http://www.cbr.ru/scripts/XML_daily.asp"


def write_data_in_xml(url):
	webFile = urllib.request.urlopen(url)
	UrlSplit = url.split("/")[-1]
	FileName = UrlSplit.replace(UrlSplit.split(".")[1], "xml")
	with open(FileName, "wb") as localFile:
		localFile.write(webFile.read())	
	webFile.close()
	return FileName

def write(date, head, currency):
	with open("exchange.txt", "w") as out:
		out.write(date)
		out.write(head)
		_str = ""
		for rate in currency:
			sid = rate.getAttribute("ID")
			charcode = rate.getElementsByTagName("CharCode")[0]
			name = rate.getElementsByTagName("Name")[0]
			value = rate.getElementsByTagName("Value")[0]
			nominal = rate.getElementsByTagName("Nominal")[0]
			_str += "{0}; {1}; {2}; {3}; {4} \n".format(
					sid,
					nominal.firstChild.data,
					name.firstChild.data,
					charcode.firstChild.data,
					value.firstChild.data
				)
		out.write(_str)

def construct_data():
	doc = minidom.parse(write_data_in_xml())
	root = doc.getElementsByTagName("ValCurs")[0]
	date = "Текущий курс валют на {date}г. \n".format(date=root.getAttribute('Date'))
	head = "Идентификатор; Номинал; Валюта; Сокращение; Курс (руб) \n"
	currency = doc.getElementsByTagName("Valute")
	write(date, head, currency)