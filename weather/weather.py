
from asyncio import exceptions
from sys import exec_prefix
import requests as r
appid = ""                                                                                        #Enter your Open weather APPID between quotes
data = {}
city_ids = []
usertype = 0
ranges=[(0,22.5),(22.6,67.5),(67.6, 112.5),(112.6,157.5),(157.6,202.5),(202.6,247.5),(247.6,292.5),(292.6,337.5),(337.6, 360)]
wind_degr = {(337.6, 360):"N",(0,22.5):"N",(22.6,67.5):"NE",(67.6, 112.5):"E",(112.6,157.5):"SE",(157.6,202.5):"S",(202.6,247.5):"SW",(247.6,292.5):"W",(292.6,337.5):"NW"}

def deg_to_winddir(deg,ranges):
    for r_start, r_end in ranges:
        if r_start <= deg <= r_end:
            return (r_start, r_end)

def more_inf(city_ids, usertype):
    cityid = city_ids[usertype - 1]
    result = r.get("http://api.openweathermap.org/data/2.5/forecast", params={'id': cityid, 'units': 'metric','lang':'ru', 'APPID': appid})
    return result.json()

def get_data(usertype):
    result=r.get("http://api.openweathermap.org/data/2.5/find", params={'q': usertype, 'type': 'like', 'units': 'metric','lang':'ru', 'APPID': appid})
    return result.json()
    
def output(usertype, data, wind_degr, ranges):
    if isinstance(usertype, int):
        usertype -= 1
        c=(len(data['list']))-1
        smp_acsess=data['list']
        for i in range(c):
            print(f"------------------------------{smp_acsess[i]['dt_txt']}------------------------------")
            print(f"| Temperature: {smp_acsess[i]['main']['temp']} C, Feels like: {smp_acsess[i]['main']['feels_like']} C")
            print(f"| Wind speed: {smp_acsess[i]['wind']['speed']} m\s, Wiind direction: {wind_degr[deg_to_winddir(smp_acsess[i]['wind']['deg'],ranges)]}")
            print(f"| Sky description: {smp_acsess[i]['weather'][0]['description']} \\ Humidity: {smp_acsess[i]['main']['humidity']}%")
        
    else:
        a = len(data['list'])
        for i in range(a):
            city_ids.append(data['list'][i]['id'])
            print("Chosen city information", data['list'][i]['id'], data['list'][i]['name'], data['list'][i]['sys']['country'], data['list'][i]['main']['temp'],"celsius")
  
print("------------------------------WEATHER CHECK PRROGRAM------------------------------")
print("To exit type: 'exit'")
    
while usertype != "exit":
    try:
        usertype = input("Enter the city where you want to receive weather information: ")
        if usertype.isdigit():
            usertype = int(usertype)
            data = more_inf(city_ids, usertype)
            output(usertype, data, wind_degr, ranges)
        else:
            if usertype == "exit":
                break
            data = get_data(usertype)
            output(usertype, data, wind_degr, ranges)

            
    except Exception as e:
        print("You do something wrong! Error name: ")
        print(e)
        
        
    