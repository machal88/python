from ftplib import FTP
import requests
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    # Pobranie danych z API OpenWeatherMap
    #api_key = 'YOUR_API_KEY'
    url = "https://api.openweathermap.org/data/2.5/weather?q=London,pl&appid={your_api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    # Wyodrębnienie temperatury
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    temp_max = data["main"]["temp_max"]
    temp_min = data["main"]["temp_min"]
    feels_like = data["main"]["feels_like"]
    
    # Wysłanie danych na serwer FTP
    ftp = FTP('ftp.example.com')
    ftp.login(user=os.getenv('FTP_USERNAME'), passwd=os.getenv('FTP_PASSWORD'))
    with open('index.html', 'w') as f:
        f.write(f'Temperature in London: {temperature} &deg;C<br>')
        f.write(f'Humidity: {humidity}%<br>')
        f.write(f'Pressure: {pressure} hPa<br>')
        f.write(f'Max temperature: {temp_max} &deg;C<br>')
        f.write(f'Min temperature: {temp_min} &deg;C<br>')
        f.write(f'Feels like: {feels_like} &deg;C<br>')
    with open('index.html', 'rb') as f:
        ftp.storbinary(f'STOR /public_html/index.html', f)
    ftp.quit()

# Przekazanie danych do szablonu HTML i wyświetlenie ich na stronie
    return render_template('index.html', temperature=temperature, humidity=humidity, pressure=pressure, temp_max=temp_max, temp_min=temp_min, feels_like=feels_like)

if __name__ == '__main__':
    app.run()

# plik .env w glownym katalogu apki
# FTP_USERNAME=username
# FTP_PASSWORD=password