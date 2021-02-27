import requests
from tkinter import *
import urllib
from PIL import ImageTk, Image
import time


class WeatherApp():
    """ A Weather App GUI"""

    def __init__(self, master=None):

        self.master = master
        master.title("Jacob's Weather App")
        #self.home_page()

    def get_zipcode(self):
        """ Retrieves a zip code from the entry box and uses the zip code to send a request to the open weather api
        """

        global zipcode
        zipcode = self.entry.get()

        # After getting the zip code, destroy the tkinter window and launch the weather page
        self.master.destroy()
        self.master = Tk()
        WeatherApp(self.master)
        self.display_weather(zipcode)
        

    def home_page(self):
        """ Launches the homepage that asks the user for their zipcode
        """

        self.label = Label(self.master, text='Enter your zip code:').grid(row=4, column=0)
        self.entry = Entry(self.master, width=10)
        self.entry.grid(row=4, column=1)
        self.button = Button(self.master, text='Go', command= self.get_zipcode).grid(row=4, column=2)


    def load_weather(self, weather):
        """
        param weather, loads the weather page
        """

        temp = weather['temp']
        feels_like = weather['feels_like']
        humidity = weather['humidity']

        # Creates a degree sign character
        degree = u'\N{DEGREE SIGN}'

        # adds the temperature
        self.label1 = Label(self.master, text=f'{"Temperature: " :<15}').grid(row=0, column=0)
        self.label2 = Label(self.master, text=str(temp) + degree + 'F').grid(row=0, column=1)

        self.label3 = Label(self.master, text=f'{"Feels Like: " :<20}').grid(row=1, column=0)
        self.label4 = Label(self.master, text=str(feels_like) + degree + 'F').grid(row=1, column=1)

        self.label5 = Label(self.master, text=f'{"Humidity: " :<21}').grid(row=2, column=0)
        self.label6 = Label(self.master, text=str(humidity) + '%').grid(row=2, column=1)

        image_id = weather['image']
        image_url = f'http://openweathermap.org/img/wn/{image_id}@2x.png'
        raw_data = Image.open(urllib.request.urlopen(image_url))

        # Store the image so it doesn't get swept up
        self.rendered_im = ImageTk.PhotoImage(raw_data)
        self.label7 = Label(self.master, image=self.rendered_im).grid(row=0, column=2, rowspan=3, columnspan=2)
        #self.button = Button(master, text='Refresh', command=self.refresh_page).grid(row=3, column=0, columnspan=2)
        self.end_button = Button(self.master, text='End', command=self.master.destroy).grid(row=4, column=3)


    def get_current_weather(self, zipcode):
        """ Sends a request to the OpenWeatherMap Api for the current weather in a current zip code
            Returns a dictionary with various attributes about the current weather
        """

        api = '1919d00de9f9a872d7bb9e85a63a94ec'

        url = 'https://api.openweathermap.org/data/2.5/weather?zip={}&appid={}&units=imperial'
        r = requests.get(url.format(zipcode, api))
        data = r.json()

        # Contains the main temperature data
        main = data['main']
        # Contains descriptive temperature data
        desc = data['weather'][0]
        # Contains the wind data
        wind = {'wind': data['wind']['speed']}

        temp = {'temp': main['temp'], 'feels_like': main['feels_like'],
                'humidity': main['humidity'], 'general': desc['main'], 'specific': desc['description'],
                'image': desc['icon'], 'wind': data['wind']['speed']}

        return temp

    def display_weather(self, zipcode):
        """ Uses the current_weather function to retrieve the current weather for a given zipcode
        """

        global weather
        weather = self.get_current_weather(zipcode)
        self.load_weather(weather)