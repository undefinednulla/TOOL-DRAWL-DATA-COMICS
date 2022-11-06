import requests
from bs4 import BeautifulSoup
import json
from printColor import *
import time

secondsStartSec = time.time()

# tìm link thể loại truyện để crawl lưu vào listTheloai
response = requests.get("https://www.nettruyenin.com/")
data = BeautifulSoup(response.content,'html.parser')
theloai = data.findAll('a',target='_self')
listTheloai = []
for item in theloai:
    list = item.get('href')
    if 'tim-truyen/' in list:
        listTheloai.append(list)


#điền vào các biến sau để crawl data từ nettruyen



userInput = 0
while True:
    try:
        url = input("Please Enter Url: ")
        pageCount = int(input("Please Enter Page Count: "))  
        nameJson = input("Please Enter Name Of .json: ")
        headerDataInput = input("Please Enter Header Of Data: ")
    except ValueError:
        print(Fore.RED + Style.NORMAL  +"Value Error! Try Again")
        continue
    else:
        print(Fore.BLUE + Style.BRIGHT+"\nStart Crawling {} Page On Nettruyenin.com\n".format(pageCount))
        break 
fileJson = nameJson + '.json'
headerJson = '{"'+headerDataInput+'": ['

i = 0
id = 0
with open(fileJson, "w") as outfile:
    outfile.write(headerJson)
while i <= pageCount:
    secondsStart = time.time()
    i=i+1
    link =  url+'?page='+ str(i)
    response = requests.get(link)
    data = BeautifulSoup(response.content,'html.parser')

    links = data.findAll('a',class_="jtip")
        
    for link in links:
        res = requests.get(link.get('href'))
        dataItem = BeautifulSoup(res.content,'html.parser')
        name = dataItem.find('h1',class_="title-detail").text
        def not_arrt(arrt):
            return arrt is None
        img = dataItem.find('img', class_=not_arrt, style=not_arrt).get("src")

        author = dataItem.find('li', class_='author row').a

        type = dataItem.findAll('p', class_='col-xs-8')[2]
        
        otherName =  dataItem.find('h2', class_='other-name col-xs-8')

        description = dataItem.find('div', class_='detail-content')

        chapter =  dataItem.find('div', class_='col-xs-5 chapter')
        chapter = chapter.text
        chapter = chapter.replace(':','')
        chapter = chapter.split()
        chapter = chapter[1]
        chapter = int( float(chapter))
        

        with open(fileJson, "a+") as outfile:

            outfile.write('{"id":')
            outfile.write(str(id))

            outfile.write(',"name":')
            json.dump(name, outfile)

            outfile.write(',"otherName":')
            if otherName is None:
                outfile.write('null')
            else:
                otherName = otherName.text
                json.dump(otherName, outfile)

            outfile.write(',"srcImg":')
            json.dump(img, outfile)

            outfile.write(',"chap":')
            json.dump(chapter, outfile)

            outfile.write(',"author":')
            if author is None:
                outfile.write('null')
            else:
                author = author.text
                json.dump(author, outfile)

            outfile.write(',"description":')
            if description is None:
                outfile.write('null')
            else:
                description = description.p
                description = description.text
                json.dump(description, outfile)

            outfile.write(',"types":')
            types = []
            for item in type:
                if '-' not in item:
                    itemtemp = item.text
                    types.append(itemtemp)
            json.dump(types, outfile)
            if i == pageCount+1 and link == links[len(links)-1] :
                outfile.write('')
            else: 
                outfile.write('},')
        id=id+1
    
    secondsEnd = time.time()
    seconds = secondsEnd-secondsStart
    sec = time.localtime(secondsEnd - secondsStart).tm_sec
    min = time.localtime(secondsEnd - secondsStart).tm_min

    print(Fore.GREEN + Style.NORMAL  +"Susseclly Crawl Page: {}/{}".format(i,pageCount)+ Style.RESET_ALL+Fore.YELLOW + Style.NORMAL+" Time: {}s".format(sec))

with open(fileJson, "a+") as outfile:
    outfile.write('}]}')

secondsEndSec = time.time()
secondsSec = time.localtime(secondsEndSec - secondsStartSec).tm_sec
secondsMin = time.localtime(secondsEndSec - secondsStartSec).tm_min

print(Fore.GREEN + Style.BRIGHT + "\nSusseclly Crawl Data Form Nettruyenin.com!" + Style.RESET_ALL + Fore.RED +"{}" + Style.RESET_ALL + Fore.GREEN +" Comic Crawled. Timeout:" + Style.RESET_ALL + Fore.RED +" {}'{}s".format(id+1,secondsMin,secondsSec))

