from lxml import html
import requests
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from time import sleep, strftime, gmtime

geolocator = Nominatim()
current_location = geolocator.geocode("Alytus, Lithuania")
coord_c_loc=(current_location.latitude, current_location.longitude)
    
def distance(city):
    auto_location = geolocator.geocode(city+', Lithuania')
    try:
        coord_a_loc=(auto_location.latitude, auto_location.longitude)
    except AttributeError:
        print('AttributeError')
        pass 
    return vincenty(coord_c_loc, coord_a_loc).km

car = input('Modelis (pirmoji raide turi buti didzioji): ')
maxdistance = input('Maksimalus atstumas nuo Alytaus (km): ')
data = strftime("%Y-%m-%d %Hh%Mm%Ss", gmtime())+' ('+car+').txt'
file = open(data, 'a', encoding='utf-8')            
pricemin= input('Maziausia kaina: ')
pricemax= input('Didziausia kaina: ')
headers = { 'User-Agent': 'Script' }
print('I tekstini faila rasomi visi galimi modeliai. Tai gali uztrukti kelias minutes.')

for i in range (1,20):
    url='https://autoplius.lt/skelbimai/naudoti-automobiliai?page_nr='+str(i)+'&sell_price_from='+pricemin+'&sell_price_to='+pricemax
    page=requests.get(url, headers = headers)
    tree = html.fromstring(page.content)
    model = tree.xpath('//*[@id="autoplius"]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/ul[1]/li/div/div[2]/h2/a/text()')
    price = tree.xpath('//*[@id="autoplius"]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/ul[1]/li/div/div[2]/div[1]/p/strong/text()')
    city = tree.xpath('//*[@id="autoplius"]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/ul/li/div/div[2]/div[2]/div/span[@title="Miestas"]/text()')
    link = tree.xpath('//*[@id="autoplius"]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/ul/li/div/div[2]/h2/a/@href')
    for j in range(len(model)):
        if (car in model[j]):
            sleep(1)
            length=distance(city[j])
            if (length<int(maxdistance)):
                result = '\nModelis: '+model[j]+'\nKaina: '+price[j]+'\nVieta: '+city[j]+' ('+str(length)+' km nuo Alytaus)\nNuoroda: '+link[j]+'\n'
                file.write(result)
            

for i in range(1, 20):
    pagename='https://autogidas.lt/automobiliai/'+str(i)+'-psl/?f_215='+pricemin+'&f_216='+pricemax+'&f_50=kaina_asc'
    page = requests.get(pagename)
    tree = html.fromstring(page.content)
    model = tree.xpath('//div[@class="item-title"]/text()') 
    price = tree.xpath('//div[@class="item-price"]/text()') 
    fixed_price = [l.strip() for l in price if l.strip()] #removes WS
    city = tree.xpath('/html/body/div[1]/div[6]/div/div[2]/a/div/div[1]/div[1]/text()')
    link = tree.xpath('/html/body/div[1]/div[6]/div/div[2]/a/@href')
    for j in range(1, len(model)):
        if (car in model[j]):
            sleep(1)
            length=distance(city[j])
            if (length<int(maxdistance)):
                result = '\nModelis: '+model[j]+'\nKaina: '+fixed_price[j]+'\nVieta: '+city[j]+' ('+str(length)+' km nuo Alytaus)\nNuoroda: https://autogidas.lt'+link[j]+'\n'
                file.write(result)
 
file.close()
print ('done')
