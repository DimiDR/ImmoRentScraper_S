# -*- coding: utf-8 -*-
import scrapy
import json, urllib.request
from immospider.items import ImmoscoutItem
import requests

class ImmoscoutSpider(scrapy.Spider):
    name = "immoscout"
    allowed_domains = ["immobilienscout24.de"]

    # The immoscout search results are stored as json inside their javascript. This makes the parsing very easy.
    # I learned this trick from https://github.com/balzer82/immoscraper/blob/master/immoscraper.ipynb .
    script_xpath = './/script[contains(., "IS24.resultList")]' #JavaScript on search list page
    next_xpath = '//div[@id = "pager"]/div/a/@href' #go to next page

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):

        #print(response.url)

        for line in response.xpath(self.script_xpath).extract_first().split('\n'):
            if line.strip().startswith('resultListModel'):
                immo_json = line.strip()
                immo_json = json.loads(immo_json[17:-1]) # everything element including #18..(last-1)

                #TODO: On result pages with just a single result resultlistEntry is not a list, but a dictionary.
                #TODO: So extracting data will fail.
                for result in immo_json["searchResponseModel"]["resultlist.resultlist"]["resultlistEntries"][0]["resultlistEntry"]:

                    item = ImmoscoutItem() #define new field if needed here

                    data = result["resultlist.realEstate"]
                    
                    #General Information
                    item['immo_id'] = data['@id']
                    item['title'] = data['title']
                    item['url'] = response.urljoin("/expose/" + str(data['@id']))
                    item['retype'] = data['@xsi.type']
                    #Adress
                    address = data['address']
                    try:
                        item['address'] = address['city'] + " " + address['street'] + " " + address['houseNumber'] 
                    except:
                        item['address'] = ""  
                    item['city'] = address['city']
                    try:
                        item['street'] = address['street']
                    except:
                        item['street'] = ""
                    try:
                        item['housenumber'] = address['houseNumber']
                    except: 
                        item['housenumber'] = ""
                    if "preciseHouseNumber" in data:
                        item['precisehousenumber'] = address['preciseHouseNumber']
                    else:
                        item['precisehousenumber'] = ""
                    item['zip_code'] = address['postcode']
                    item['district'] = address['quarter']
                    try:
                        item['lat'] = address['wgs84Coordinate']['latitude']
                        item['lng'] = address['wgs84Coordinate']['longitude']
                    except Exception as e:
                        # print(e)
                        item['lat'] = ""
                        item['lng'] = ""
                    #Additions
                    if "balcony" in data:
                        item["balcony"] = data["balcony"]
                    else:
                        item["balcony"] = ""
                    if "builtInKitchen" in data:
                        item["kitchen"] = data["builtInKitchen"]
                    else:
                        item["kitchen"] = ""
                    if "cellar" in data:
                        item["cellar"] = data["cellar"] 
                    else:
                        item["cellar"] = ""
                    if "companywidecustomerid" in data:
                        item['companywidecustomerid'] = address['companyWideCustomerId']
                    else:
                        item["companywidecustomerid"] = ""
                    #contactDetails
                    contact = data['contactDetails']
                    try:
                        item['contcompany'] = contact['company']
                    except:
                        item['contcompany'] = ""
                    try:
                        item['contname'] = contact['firstname'] + " " + contact["lastname"]
                    except:
                        item['contname'] = ""
                    if "contfirstname" in data:
                        item['contfirstname'] = contact['firstname']
                    else:
                        item['contfirstname'] = ""
                    if "contlastname" in data:
                        item['contlastname'] = contact['lastname']
                    else:
                        item['contlastname'] = ""
                    if "contphonenumber" in data:
                        item['contphonenumber'] = contact['phoneNumber']
                    else:
                        item['contphonenumber'] = ""
                    item['contsalutation'] = contact['salutation']
                    #courtage
                    #courtage = data['courtage']
                    #item['hascourtage'] = courtage['hasCourtage']
                    item['hascourtage'] = ''
                    #Additions2
                    item['floorplan'] = data['floorplan']
                    if "garden" in data:
                        item["garden"] = data["garden"]
                    else:
                        item["garden"] = ""
                    if "guestToilet" in data:
                        item["guesttoilet"] = data["guestToilet"]
                    else:
                        item["guesttoilet"] = ""
                    if "isBarrierFree" in data:
                        item["isbarrierfree"] = data["isBarrierFree"]
                    else:
                        item["isbarrierfree"] = ""
                    if "lift" in data:
                        item["lift"] = data["lift"]
                    else:
                        item["lift"] = ""
                    item["listingtype"] = data["listingType"]
                    item["livingspace"] = data["livingSpace"]
                    item["numberofrooms"] = data["numberOfRooms"]
                    #price
                    price = data["price"]
                    item["currency"] = price["currency"]
                    item["marketingtype"] = price["marketingType"]
                    item["priceintervaltype"] = price["priceIntervalType"]
                    item["value"] = price["value"]
                    #Additions3
                    if "privateOffer" in data:
                        item["privateoffer"] = data["privateOffer"]
                    else:
                        item["privateoffer"] = ""
                    try:                    
                        item["realtorcompanyname"] = data["realtorCompanyName"]
                    except:
                        item["realtorcompanyname"] = ""
                    if "realtorlogo" in data:
                        item["realtorlogo"] = data["realtorLogo"]
                    else:
                        item["realtorlogo"] = ""
                    item["spotlightlisting"] = data["spotlightListing"]
                    item["streamingvideo"] = data["streamingVideo"]
                    #titlePicture
                    try: 
                        titlePicture = data["titlePicture"]
                    except:
                        titlePicture = ""
                    try: 
                        item["creation"] = titlePicture["@creation"]
                    except:
                        item["creation"] = ""

                    try:
                        item['media_count'] = len(data['galleryAttachments']['attachment'])
                    except:
                        item['media_count'] = 0
                    
                    yield item

        next_page_list = response.xpath(self.next_xpath).extract()
        if next_page_list:
            next_page = next_page_list[-1]
            print("Scraping next page", next_page)
            if next_page:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
