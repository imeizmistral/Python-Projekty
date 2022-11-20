from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#Dane dotyczące kursu Dolara
DaneDolar = pd.DataFrame()
url = "https://www.biznesradar.pl/notowania-historyczne/USDPLN"
t= 12
for k in range(1,t):
   page = url+','+ str(k)

   dolarPage = requests.get(page)
   soupDolar = BeautifulSoup(dolarPage.text, 'html.parser')
   soupDolar
   
   table1 = soupDolar.find('table')
   table1

   headers = []
   for i in table1.find_all('th'):
    title = i.text
    headers.append(title)
    
   mydata = pd.DataFrame(columns=headers)
  

   for j in table1.find_all('tr')[1:]:
    row_data = j.find_all('td')
    row = [i.text for i in row_data]
    length = len(mydata)
    mydata.loc[length] = row
    
   DaneDolar = DaneDolar.append(mydata)
   
DaneDolar["Data"] = pd.to_datetime(DaneDolar["Data"], format="%d.%m.%Y")
DaneDolar["Zamknięcie"] = pd.to_numeric(DaneDolar['Zamknięcie'])

  
 #Dane dotyczące kursu barłyki Ropy Brent
DaneOil = pd.DataFrame()
url = "https://www.biznesradar.pl/notowania-historyczne/BRENT-OIL-ROPA-BRENT"
t= 12
for k in range(1,t):
    page = url+','+ str(k)

    OilPage = requests.get(page)
    soupOil = BeautifulSoup(OilPage.text, 'html.parser')
    soupOil
    
    table1 = soupOil.find('table')
    table1

    headers = []
    for i in table1.find_all('th'):
     title = i.text
     headers.append(title)
     
    mydata = pd.DataFrame(columns=headers)
   

    for j in table1.find_all('tr')[1:]:
     row_data = j.find_all('td')
     row = [i.text for i in row_data]
     length = len(mydata)
     mydata.loc[length] = row
     
    DaneOil = DaneOil.append(mydata)
    
DaneOil["Data"] = pd.to_datetime(DaneOil["Data"], format="%d.%m.%Y")
DaneOil["Zamknięcie"] = pd.to_numeric(DaneOil['Zamknięcie'])
 
 
 # Dane dotyczące sredniej ceny benzyny 95 na stacjach w Polsce
url3 = "https://www.bankier.pl/gospodarka/wskazniki-makroekonomiczne/eu-95-pol"
Pb95Page = requests.get(url3)
soup95 = BeautifulSoup(Pb95Page.content, 'html.parser')
soup95
 # Pb95
table3 = soup95.find('div', id='pageSubContainerRight315')
table3

headers = []
for i in table3.find_all('th'):
 title = i.text
 headers.append(title)

mydata3 = pd.DataFrame(columns=headers)
mydata3

for j in table3.find_all('tr')[1:]:
 row_data = j.find_all('td')
 row = [i.text for i in row_data]
 length = len(mydata3)
 mydata3.loc[length] = row
  
  
mydata3['Data'] = mydata3['Data'].str.strip().str[-10:]

mydata3["Data"] = pd.to_datetime(mydata3["Data"], format="%Y-%m-%d")
res=[]
for i in mydata3.Wartość:
 res.append(i.replace(",", "."))
mydata3["Wartość"] = res
mydata3["Wartość"] = pd.to_numeric(mydata3['Wartość'])
mydata3.info()

d = mydata3['Data'] >= min(DaneDolar['Data'])
mydata3 = mydata3.loc[d]
 
#Ploty
col1 = 'steelblue'
col2 = 'red'
col3 = 'green'

 #define subplots
fig,ax = plt.subplots()

 #add first line to plot
ax.plot(DaneDolar.Data, DaneDolar.Zamknięcie, color=col1,label="Kurs dolara")
ax.plot(mydata3.Data, mydata3.Wartość, color=col3,label="Cena na stacjach PB95")
ax.axvline(x=['2022-02-01'],color='gray', linestyle='--', label="Tarcza antyinflacyjna")
ax.axvspan(xmin='2022-06-24',xmax='2022-09-15', alpha=0.5, color='yellow', label="30 gr mniej")
plt.legend()
 #add x-axis label
ax.set_xlabel('Data', fontsize=14)
plt.xticks(rotation = 45)


 #add y-axis label
ax.set_ylabel('PLN', color=col1, fontsize=16)

 #define second y-axis that shares x-axis with current plot
ax2 = ax.twinx()

 #add second line to plot
ax2.plot(DaneOil.Data, DaneOil.Zamknięcie, color=col2,label="Cena za baryłkę")
plt.legend(loc='lower right')
 #add second y-axis label
ax2.set_ylabel('USD', color=col2, fontsize=16)

ax.set_title("Stosunek cen hurtowych do realnej ceny zakupu paliwa PB95")

 