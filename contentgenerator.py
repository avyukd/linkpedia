
#exec(open('linkpedia/contentgenerator.py').read())
from linkpedia.models import Datapoint, Link
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import random
url = 'https://en.wikipedia.org/wiki/Special:AllPages/'
countries = open('C:/Users/Avyuk Dixit/countries.txt').read().split("\n")
nop = 50
app = 3
letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
print('ok')
for n in range(0,nop,1):
	letter1 = letters[random.randint(0,25)].upper()
	letter2 = letters[random.randint(0,25)]
	nexturl = url+letter1+letter2
	source_code  = requests.get(url)
	plain =  source_code.text
	soup = BeautifulSoup(plain, 'html.parser')
	print('hello')
	ints = []
	for i in range(0,app):
		ints.append(random.randint(1,100))
	f = 0
	for link in soup.findAll('a',{'class':'mw-redirect'}):		
		if f in ints:
			datapointurl = 'https://en.wikipedia.org' + link.get('href')
			dpcode  = requests.get(url)
			dplain =  dpcode.text
			dpsoup = BeautifulSoup(dplain, 'html.parser')
			title= dpsoup.findAll('h1')[0]
			time = datetime.now()
			dictionary = {}
			for next in dpsoup.findAll('h3'):
				for coun in countries:
					if coun in next:
						if coun in dictionary.keys():
							dictionary[coun]+=1
						else:
							dictionary[coun] = 1
			max_entry = ""
			max_value = 0
			for k,v in dictionary:
				if v > max_value:
					max_value = v
					max_entry = k
			country= max_entry
			url = datapointurl
			print(dplain)
			print("all: ", plain.find('<p>'))
			desc = dpsoup.findAll('p')[0]
			
			print(title, time, country, url, desc)
			
		f+=1
	
	#Datapoint.objects.create(timestamp=datetime.now(),country='country2',data_url='data_url2',data_title='data_title2',data_description='data_description2')


