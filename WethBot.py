import telebot
import requests
from datetime import datetime
from config import api_key
from config import token

bot = telebot.TeleBot(token)

def get_data(city):
    try:
        req = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}")
        geo = req.json()
        req = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={geo[0]['lat']}&lon={geo[0]['lon']}&appid={api_key}")
        weather = req.json()
        return weather
    except:
        return 0

@bot.message_handler(commands='start')
def start_message(message):
    user_name = message.chat.username
    bot.send_message(message.chat.id, f"Hello {user_name}! To get weather data, type 'weather [location]'\n(ex.: 'weather London')")

@bot.message_handler(content_types=['text'])
def send_data(message):
    inp = list(message.text.split())
    if inp[0] == 'weather':
        city = inp[1]
        try:
            weather_date = get_data(city)

            date = datetime.now().strftime('%Y-%m-%d %H:%M')
            weather = weather_date['weather'][0]['description']
            temp = int(weather_date['main']['temp']) - 273
            wind = weather_date['wind']['speed']
            humidity = weather_date['main']['humidity']

            bot.send_message(message.chat.id, f"City:   {city}\nDate:   {date}\nWeather:    {weather}\nTemp:   {temp}°C\nHumidity:   {humidity}%\nWind:   {wind} m/s")
        except:
            bot.send_message(message.chat.id, "Error: Check the input data.")

if __name__ == '__main__':
    bot.polling()