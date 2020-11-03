'''
This program is scraping items's data from https://bbcart-com.myshopify.com website.
This data is scraped for B2B ecommerce company eWhale.co for their internal verificatiion of items hosted on site.

@author Karishma Sukhwani
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd


main_url = "https://bbcart-com.myshopify.com/collections/skin-care"
response = requests.get(main_url)
soup = BeautifulSoup(response.text, 'lxml')

titleList = []
vendorList = []
retailPriceList = []
disPriceList = []
inStockList = []
imgLinkList = []
catList = []

#Add all sub urls of /skin_care web page using pagination
pages = soup.find('div', class_='pagination text-center')
urls = []
links = pages.find_all('span', class_='page')
#print(links)
lastPageNo = None

for link in links:
    lastPageNo = int(link.text)

#print(lastPageNo)

for i in range(1, lastPageNo+1):
    urls.append(main_url + "?page=" + str(i))

#add 2 more links for personal-care items and hair-care
urls.append("https://bbcart-com.myshopify.com/collections/personal-care")
urls.append("https://bbcart-com.myshopify.com/collections/hair-care")


#retrive/ scrape all the pages using BeautifulSoup for all item datails page by page
for url in urls:
    print("for url: {}".format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    cat = ""
    if(url.startswith("https://bbcart-com.myshopify.com/collections/skin-care")):
        cat = "skin care"
    elif(url.startswith("https://bbcart-com.myshopify.com/collections/personal-care")):
        cat = "Accessories"
    else:
        cat = "Hair-care"
    
    items = soup.find_all('div', class_='product grid__item medium-up--one-third small--one-half slide-up-animation animated')

    #set item details
    for i in items:
        #name
        itemName = i.find('div', class_="product__title product__title--card text-center")
        titleList.append(itemName.text.replace('\n', ''))
        
        #vendor
        itemVendor = i.find('div', class_="product__vendor text-center")
        vendorList.append(itemVendor.text.replace('\n', '').replace('      ', ''))
        
        #price
        itemPrice = i.find('div', class_="product__prices text-center")
        rawPriceLine = itemPrice.text.replace('\n', '')
        #f.write(rawPriceLine)
        if(rawPriceLine.startswith("Sale pric")):
            inStock = "YES"
            rp = float(rawPriceLine.split("          ")[2].split(' ')[6][:-4].replace(',',''))
            retailPriceList.append(rp)
            
            dp = float(rawPriceLine.split('          ')[1].split()[1].replace(',',''))
            disPriceList.append(dp)
            
            if(rawPriceLine.endswith("Out")):
                inStock = "NO"
            
            inStockList.append(inStock)
        
        else:
            inStock = "YES"
            rp = float(rawPriceLine.split('          ')[1].split()[1].replace(',',''))
            retailPriceList.append(rp)
            
            dp = "-"
            disPriceList.append(dp)
            
            inStockList.append(inStock)
           
        
        #imageLink
        itemLink = i.find('a', class_="product__image-wrapper")
        iRes = requests.get("https://bbcart-com.myshopify.com"+itemLink.get("href"))
        iSoup = BeautifulSoup(iRes.text, 'lxml')
        tt = iSoup.find('div', class_="product-single__photos")
        tz = tt.find('img', class_="product-single__photo lazyload")
        imgLinkList.append("https://" + tz.get("src")[2:])
        #imgLinkList.append(itemLink.get("href"))
        
        #categoryList
        catList.append(cat)
        

#print(titleList)

#create a dataframe and save into excel sheet using ExcelWriter
outdf = pd.DataFrame({"Vendor Name" : vendorList, "Product Name" : titleList, "Discounted Price": disPriceList,
                         "Retail Price": retailPriceList, "Available": inStockList, "imgLink": imgLinkList, "sub category": catList})
#print(outdf)

#output file will be siteData.xlsx
writer = pd.ExcelWriter("siteData.xlsx", engine="xlsxwriter")
outdf.to_excel(writer, sheet_name = "Sheet1", index = False)
writer.save()
