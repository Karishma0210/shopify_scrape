''' 
This code will check if the given items are present on site's data or not.
There are 2 input files used, in which one file is having items to check on site and other file is for items present on the site.


givendf = pd.read_excel("input.xlsx", "Sheet1") #having 96 data row to check on site
#givendf.head(7)
siteStockdf = pd.read_excel("siteData.xlsx", "Sheet1") #having 103 data row fetched from scraper.py code
#siteStockdf
#print(len(givendf.index),
#len(siteStockdf.index))

skuList = ['-']*103 #to mention SKU name on siteData.xlsx
newssDf = siteStockdf
presentList = ['NO']*96 #is it present on the site?
newgDf = givendf
for i in range(len(givendf.index)):
    for j in range(len(siteStockdf.index)):
        if(givendf.iloc[i, 6] == siteStockdf.iloc[j, 1]):#if productname exist in both files
            
            if(givendf.iloc[i, 8] == siteStockdf.iloc[j, 3] and givendf.iloc[i, 9] == siteStockdf.iloc[j, 2]):#regprice,disprice
                #if prices mentioned are same then mark it as presentOnSite
                skuList[j] = givendf.iloc[i, 4]
                presentList[i] = "YES"
                break

#add new coloumns in dataset
newssDf["SKU"] = skuList
newgDf["PresentOnSite"] = presentList

#mention SKU on fetched 
writer = pd.ExcelWriter("siteStock-updated.xlsx", engine="xlsxwriter")
newssDf.to_excel(writer, sheet_name = "Sheet1", index = False)
writer.save()

writer = pd.ExcelWriter("input-updated.xlsx", engine="xlsxwriter")
newgDf.to_excel(writer, sheet_name = "Sheet1", index = False)
writer.save()
