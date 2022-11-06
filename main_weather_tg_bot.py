import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(
        "Hi! Send me your city name, and I'll send you your weather forecast")


@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        text = message.text
        if text == 'Angelina' or text == 'angelina' or text == 'Ангелина' or text == 'ангелина' or text == 'геля' or text == 'Геля':
            await message.reply(
                f"\U00002764 Привет солнышко! Очень люблю тебя! \U0001F495")
        else:
            ll = requests.get(
                f"http://api.openweathermap.org/geo/1.0/direct?q={text}&limit={1}&appid={open_weather_token}"
            )
            lldata = ll.json()
            r = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?lat={lldata[0]['lat']}&lon={lldata[0]['lon']}&appid={open_weather_token}&units=metric"
            )
            data = r.json()
            weather_type = data['weather'][0]['description']
            name = data['name']
            temp = data['main']['temp']
            temp_min = data['main']['temp_min']
            temp_max = data['main']['temp_max']
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
            daytime = datetime.datetime.fromtimestamp(
                data['sys']['sunset']) - datetime.datetime.fromtimestamp(
                    data['sys']['sunrise'])
            await message.reply(
                f"Weather in the city: {name} \n"
                f"Weather type {weather_type} \n"
                f"Temp {temp}, max temp {temp_max}, min temp {temp_min} \n"
                f"Hunidity {humidity} % \n"
                f"Pressure {pressure} \n"
                f"Windspeed {wind_speed} m/s \n"
                f"Sunrise {sunrise} and sunset {sunset} \n"
                f"Lenght of the day: {daytime} \n"
                f"HAVE A GOOD DAY!")
    except:
        await message.reply("Check spelling of the city name.")


if __name__ == "__main__":
    executor.start_polling(dp)
