import requests
from bs4 import BeautifulSoup
import re
import pyodbc as odbc

def show(city, price, dist):
    # Database connection settings
    DRIVER_NAME = 'SQL SERVER'
    SERVER_NAME = 'LAPTOP-BETIDGLL'
    DATABASE_NAME = 'BOT3'

    # Connection string
    connection_string = f"""
        DRIVER={{{DRIVER_NAME}}};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        TRUST_Connection=yes;
    """

    # Establish a connection to the database
    conn = odbc.connect(connection_string)

    page = 1

    if city == "Warsaw":
        dist = "Warszawa, " + dist
        url = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?page=' + str(page) + '&search%5Border%5D=created_at%3Adesc'
    if city == "Lodz":
        dist = "Łódź, " + dist
        url = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/lodz/?page=' + str(page) + '&search%5Border%5D=created_at:desc'

    response = requests.get(url)
    tree = BeautifulSoup(response.content, 'html.parser')
    html = tree.find_all('a', {'class': 'css-rc5s2u'})

    #
    links = []
    for i in range(len(html)):
        links.append(html[i].get('href'))
    #
    names = [tag.text for tag in tree.select('h6.css-16v5mdi.er34gjf0')]
    #
    pricesNum = []
    prices = [tag.text for tag in tree.select('p.css-10b0gli.er34gjf0')]
    for i in range(len(prices)):
        prices[i] = prices[i].replace("do negocjacji", " (do negocjacji)")
        pricesNum.append(" ")
        pricesNum[i] = prices[i].replace("(do negocjacji)", "")
        pricesNum[i] = pricesNum[i].replace("zł", "")
        pricesNum[i] = pricesNum[i].replace(" ", "")

    #
    districtsAndTime = [tag.text for tag in tree.select('p.css-veheph.er34gjf0')]
    districts = []
    timeAdded = []
    for i in districtsAndTime:
        parts = i.split(" - ")
        districts.append(parts[0])
        timeAdded.append(parts[1])

    for i in range(len(links)):
        if links[i].startswith("/d/"):
            links[i] = "https://www.olx.pl" + links[i]

    area = []
    NoRooms = []

    for link in links:
        if link.startswith("https://www.olx.pl"):
            response = requests.get(link)
            tree = BeautifulSoup(response.content, 'html.parser')
            info = [tag.text for tag in tree.select('p.css-b5m1rv.er34gjf0')]
            for i in range(len(info)):
                if info[i].startswith("Powierzchnia"):
                    divider = info[i].split()
                    area.append(divider[1])
                if info[i].startswith("Liczba pokoi:"):
                    divider = info[i].split()
                    NoRooms.append(divider[2])
        else:
            response = requests.get(link)
            tree = BeautifulSoup(response.content, "html.parser")
            elements = tree.find_all("div", {"class": "css-1wi2w6s"})
            divider = (elements[0].text.split())
            area.append(divider[0])
            divider = (elements[1].text.split())
            if int(divider[0]) > 4:
                divider = (elements[2].text.split())
            NoRooms.append(divider[0])

    for i in range(len(NoRooms)):
        if NoRooms[i] == "Kawalerka":
            NoRooms[i] = "1"

    priceL = 0
    priceH = 30000
    if price == "1000 - 1500":
        priceL = 1000
        priceH = 1500
    elif price == "1500 - 2000":
        priceL = 1500
        priceH = 2000
    elif price == "2000 - 2500":
        priceL = 2000
        priceH = 2500
    elif price == "2500 - 3000":
        priceL = 2500
        priceH = 3000
    elif price == "3000 - 3500":
        priceL = 3000
        priceH = 3500
    elif price == "> 3500":
        priceL = 3500
        priceH = 30000

    # send to bot
    res = []
    counter = 0

    # Create a cursor object
    cursor = conn.cursor()

    for i in range(3, 13):
        if (priceL <= int(pricesNum[i]) <= priceH) and (districts[i] == dist):
            strg = "👤 TITLE: " + names[i] + "\n\n📍 DISTRICT: " + districts[i] + "\n\n💰 PRICE: " + prices[i] + "\n\n@ ROOMS: " + NoRooms[i] + "\n\n@ AREA " + area[i] + "m2\n\n@ TIME ADDED: " + timeAdded[i] + "\n\n🔗 LINK: " + links[i]
            res.append(strg)
            counter += 1

            # Define the SQL query to insert the data into your table
            query = "INSERT INTO dbo.LodzDB2 (Title, District, Price, Rooms, Area, Time_added, Link) VALUES (?, ?, ?, ?, ?, ?, ?)"

            # Define the parameter values for the query
            parameters = (names[i], districts[i], prices[i], NoRooms[i], area[i], timeAdded[i], links[i])

            # Execute the query
            cursor.execute(query, parameters)

    for i in range(16, 26):
        if (priceL <= int(pricesNum[i]) <= priceH) and (districts[i] == dist):
            strg = "👤 TITLE: " + names[i] + "\n\n📍 DISTRICT: " + districts[i] + "\n\n💰 PRICE: " + prices[i] + "\n\n@ ROOMS: " + NoRooms[i] + "\n\n@ AREA " + area[i] + "m2\n\n@ TIME ADDED: " + timeAdded[i] + "\n\n🔗 LINK: " + links[i]
            res.append(strg)
            counter += 1

            # Define the SQL query to insert the data into your table
            query = "INSERT INTO dbo.LodzDB2 (Title, District, Price, Rooms, Area, Time_added, Link) VALUES (? ,? ,? ,? ,? ,? ,? )"

            # Define the parameter values for the query
            parameters = (names[i], districts[i], prices[i], NoRooms[i], area[i], timeAdded[i], links[i])

            # Execute the query
            cursor.execute(query, parameters)

    for i in range(29, 39):
        if (priceL <= int(pricesNum[i]) <= priceH) and (districts[i] == dist):
            strg = "👤 TITLE: " + names[i] + "\n\n📍 DISTRICT: " + districts[i] + "\n\n💰 PRICE: " + prices[i] + "\n\n@ ROOMS: " + NoRooms[i] + "\n\n@ AREA " + area[i] + "m2\n\n@ TIME ADDED: " + timeAdded[i] + "\n\n🔗 LINK: " + links[i]
            res.append(strg)
            counter += 1

            # Define the SQL query to insert the data into your table
            query = "INSERT INTO dbo.WarsawDB2 (Title, District, Price, Rooms, Area, Time_added, Link) VALUES (?, ?, ?, ?, ?, ?, ?)"

            # Define the parameter values for the query
            parameters = (names[i], districts[i], prices[i], NoRooms[i], area[i], timeAdded[i], links[i])

            # Execute the query
            cursor.execute(query, parameters)

    for i in range(42, 50):
        if (priceL <= int(pricesNum[i]) <= priceH) and (districts[i] == dist):
            strg = "👤 TITLE: " + names[i] + "\n\n📍 DISTRICT: " + districts[i] + "\n\n💰 PRICE: " + prices[i] + "\n\n@ ROOMS: " + NoRooms[i] + "\n\n@ AREA " + area[i] + "m2\n\n@ TIME ADDED: " + timeAdded[i] + "\n\n🔗 LINK: " + links[i]
            res.append(strg)
            counter += 1

            # Define the SQL query to insert the data into your table
            query = "INSERT INTO dbo.WarsawDB2 (Title, District, Price, Rooms, Area, Time_added, Link) VALUES (?, ?, ?, ?, ?, ?, ?)"

            # Define the parameter values for the query
            parameters = (names[i], districts[i], prices[i], NoRooms[i], area[i], timeAdded[i], links[i])

            # Execute the query
            cursor.execute(query, parameters)
            
            try:
                # Execute the query
                cursor.execute(query, parameters)
            except odbc.Error as e:
                print(f"Error inserting data: {e}")
                

    res.append("There are " + str(counter) + " offers")

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    result = []
    return res

