import json
import urllib.request
import Defines as d
import logging

class Get_Weather_Data():
    def __init__(self):
        pass

    def get_data(self, data_client,method_code):
        
        #requestul de pe api se face utilizand tcp
    
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=8e6e05650e8905f4aecdfaac6cea6a67'.format(data_client)
        req = urllib.request.Request(url)
        
        try:
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
            # transform in array de bytes cu decode
            json_data = json.loads(the_page)
        except:
            print("ati introdus orasul gresit")
            logging.info("ERROR 404 COULD NOT GET FROM API")
            
            return 404
            
            
        #print(json_data)
        try:
            code       = json_data['cod']
            temp       = json_data['main']['temp']
            temp_min   = json_data['main']['temp_min']
            temp_max   = json_data['main']['temp_max']
            pressure   = json_data['main']['pressure']
            humidity   = json_data['main']['humidity']
            feels_like = json_data['main']['feels_like']

            if int(method_code) == d.METHOD_CONVERT:
                temp       = round(temp - 273.15, 2)
                temp_max   = round(temp_max - 273.15, 2)
                temp_min   = round(temp_min - 273.15, 2)
                feels_like = round(feels_like - 273.15, 2)

            info_weather = str(temp)+'-'+ str(feels_like)+'-'+str(temp_min)+'-'+str(temp_max)+'-'+str(pressure)+'-'+str(humidity)
        except KeyError:
            print("error code- ", json_data["cod"])
            print("description -", json_data["message"])
        return code, info_weather

    





