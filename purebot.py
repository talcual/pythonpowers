from lxml import html  
import csv,os,json
import requests
from exceptions import ValueError
from time import sleep
from fake_useragent import UserAgent
import pprint
import re

ua = UserAgent()
 
def AmzonParser(url):
    headers = {'User-Agent': ua.random}
    page = requests.get(url,headers=headers)
    while True:
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//span[@id="productTitle"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
            XPATH_FEATURES = '//*[@id="feature-bullets"]/ul/li/*/text()'
 
            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            RAW_FEATURES = doc.xpath(XPATH_FEATURES)
 
            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
            FEATURES = ''.join(RAW_FEATURES).strip() if RAW_FEATURES else None
 
            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE
 
            if page.status_code!=200:
                raise ValueError('captcha')

            if findWholeWord('captcha')(page.content) != None:
            	print doc.xpath('/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img/@src')
                

            data = {
                    'NAME':NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'CATEGORY':CATEGORY,
                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
                    'AVAILABILITY':AVAILABILITY,
                    'FEATURES': FEATURES,
                    'URL':url,
                    }
 
            return data
        except Exception as e:
            print e
 
def ReadAsin():
    
    file = open("asinx.csv", "r") 
    AsinList = file.readlines()
    target = ''
    headers = {'content-type': 'application/json'}

    for i in AsinList:
        url = "http://www.amazon.com/dp/"+i.replace('\n','')
        print "Processing: "+url
        #print AmzonParser(url)
        r = requests.post(target, data=json.dumps(AmzonParser(url)), headers=headers)
        
        print r.text
        
        print r.elapsed.total_seconds()
        sleep(5)

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
 
if __name__ == "__main__":
    ReadAsin()
