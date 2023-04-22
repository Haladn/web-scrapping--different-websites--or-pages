from bs4 import BeautifulSoup
import requests
import re


user=str(3080 )    #input("enter the product id:")  #3080
url=f"https://www.newegg.ca/p/pl?d={user}&N=4131"
request=requests.get(url).text
soup=BeautifulSoup(request,"lxml")
pages=soup.find_all(class_="list-tool-pagination-text")[0].strong
num_pages=int(str(pages).split("/")[-2].split(">")[-1][:-1])

products={}
for page in range(1,num_pages+1):
    url = f"https://www.newegg.ca/p/pl?d={user}&N=4131&page={page}"
    request = requests.get(url).text
    soup = BeautifulSoup(request, "lxml")
    div=soup.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items=div.find_all(string=re.compile(user))
    for item in items:
        parent=item.parent

        if parent.name!="a":
            continue
        link=parent["href"]
        next=item.find_parent(class_="item-container")
        next.find(class_="price-current").contents
        if next.find(class_="price-current").contents == []:
            continue
        price=next.find(class_="price-current").contents[2].string
        products[item]={"price":int(price.replace(",","")),"link":link}

sorted_items=sorted(products.items(),key=lambda x: x[1]["price"])
for item in sorted_items:
    print(item[0])
    print(f'${item[1]["price"]}')
    print(item[1]["link"])
    print("________________________")
