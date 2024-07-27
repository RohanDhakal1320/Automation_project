## This code is used to get the weather based on the date and time and request 

import requests
import datetime

## Configuration
API_KEY = 'your_openweather_api_key' # Replace with your OpenWeather API Key
CITY = 'Nelson'
LOG_FILE = 'weather_log.txt'
API_URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

def fetch_weather():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return weather
    else:
        print("Error fetching date from the weather API.")
        return None
    
def log_weather(weather):
    with open(LOG_FILE, 'a') as file:
        file.write(f"{weather['date']} - {weather['city']}: {weather['temperature']}C, {weather['description']}\n")
        
def main():
    weather = fetch_weather()
    if weather:
        log_weather(weather)
        print(f"logged weather data for {weather['city']}.")
        
if __name__ == "__main__":
    main()
    