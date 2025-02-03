import requests  
from bs4 import BeautifulSoup
import re
    
link = "https://www.olx.pl/d/oferta/kawalerka-w-centrum-lodzi-20-m2-kilinskiego-16-CID3-IDJeYt6.html"
    
if link.startswith("https://www.olx.pl"):
    response = requests.get(link)
    tree = BeautifulSoup(response.content, 'html.parser')
    info = [tag.text for tag in tree.select('p.css-b5m1rv.er34gjf0')]
    print(info)
    for i in range(len(info)):
                if info[i].startswith("Liczba"):
                    divider = info[i].split()
                    print("=" + divider[2] + "=")
else:
    response = requests.get(link)
    tree = BeautifulSoup(response.content, "html.parser")
    elements = tree.find_all("div", {"class": "css-1wi2w6s"}) 
    print(elements)
    divider = (elements[1].text.split())
    print(divider[0])
    
