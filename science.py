import requests
from bs4 import BeautifulSoup

def get_weather():
    try:
        # Replace with the appropriate city and API key
        city = "Kamloops"  
        api_key = "5bd569ef15994e94db0132c4cf485649"
        
        # Construct the API URL
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        # Make the request to the OpenWeatherMap API
        response = requests.get(url)
        
        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            
            # Extract relevant weather data from the response
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            
            # Format the response message
            weather_info = f"Weather in {city}:\n" \
                           f"Description: {weather_description}\n" \
                           f"Temperature: {temperature}°C\n" \
                           f"Humidity: {humidity}%\n" \
                           f"Wind Speed: {wind_speed} m/s"
            
            return weather_info
        else:
            return "Unable to fetch weather information at the moment."
    except Exception as e:
        return f"Error: {str(e)}"
