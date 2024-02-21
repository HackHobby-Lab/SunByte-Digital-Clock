from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
import requests
from kivy.config import Config 
from kivy.graphics import Color,Rectangle
from pinpong.board import *
from pinpong.extension.unihiker import *
from kivy.core.window import Window

Board().begin()  # Initialize the UNIHIKER

count = 100
class DigitalClock(App):
    def build(self):
        
        self.layout = FloatLayout()
        # This following section plays the video as background. But it does not render good result on unihiker
        # self.video = Video(source="background/ghost.mp4", state='play', fit_mode='fill', volume=0, color=[1,1,1],  options={'eos' : 'loop'})
        # self.layout.add_widget(self.video)
        self.ghost = Image(source="background/ghost.jpg",fit_mode='fill')
        self.layout.add_widget(self.ghost)

        # Add your other widgets
        self.label2 = Label(
            text="HACKHOBBY LAB",
            font_size=10,
            pos_hint={'center_x': 0.5, 'center_y': 0.03},    
            markup=True
        )
        self.label = Label(
            text="00:00:00 AM",
            font_size=40,
            #font_name='C:/Users/Awan/fonts/SinkinSans-200XLight.otf',
            halign='center',
            markup=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        self.labelDate = Label(
            text="[color=FFFF00]January 1, 2024[/color]",
            font_size=15,
            font_name='fonts/SinkinSans-500Medium.otf',
            markup=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.61}
        )

        self.labelCity = Label(
            text="",
            font_size=18,
            font_name='fonts/SinkinSans-200XLight.otf',
            pos_hint={'center_x': 0.5, 'center_y': 0.85},
            markup=True
        )

        self.labelTemp = Label(
            text="",
            font_size=18,
            font_name='fonts/SinkinSans-500Medium.otf',
            pos_hint={'center_x': 0.3, 'center_y': 0.5},
            markup=True
        ) 

        self.labelHumidity = Label(
            text="",
            font_size=18,
            font_name='fonts/SinkinSans-500Medium.otf',
            pos_hint={'center_x': 0.78, 'center_y': 0.5},
            markup=True
        )

        self.labelDescription = Label(
            text="",
            font_size=18,
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            markup=True
        )
        
        
        icon_path = "icons/therm.png"  
        therm_icon = Image(source=icon_path,  pos_hint={'center_x': 0.16, 'center_y': 0.5}, size_hint=(0.08,0.08))

        icon_path = "icons/hygrometer.png"  
        hygro_icon = Image(source=icon_path,  pos_hint={'center_x': 0.65, 'center_y': 0.5}, size_hint=(0.08,0.08))


        self.layout.add_widget(therm_icon)
        self.layout.add_widget(hygro_icon)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.labelDate)
        self.layout.add_widget(self.label2)
        self.layout.add_widget(self.labelCity)
        self.layout.add_widget(self.labelTemp)
        self.layout.add_widget(self.labelHumidity)
        self.layout.add_widget(self.labelDescription)

        self.update_weather()
        Clock.schedule_interval(self.orientation, 0.2)
        Clock.schedule_interval(self.brightness, 0.2)
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.update_weather, 600)  # 600 seconds = 10 minutes

        return self.layout

    def update_time(self, interval):
        self.label.text = self.get_time()
        self.labelDate.text = self.get_date()

    def get_time(self):
        import time
        current_time = time.strftime('[color=FFFFFF]%I[/color]:[color=FFFFFF]%M[/color][size=10]:[color=FFFFFF]%S[/size][/color][color=FFFFFF]%p[/color]')
        return current_time
    def get_date(self):
        import time
        current_date = time.strftime('[color=FFFF00]%B %d, %Y[/color]')
        return current_date
    def update_weather(self, *args):
        # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
        api_key = 'Your API Key Goes here'
        city_name = 'Multan'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'

        try:
            response = requests.get(url, timeout=5)  
            if response.status_code == 200:
                data = response.json()

                # Extract necessary weather information
                temperature = data['main']['temp']
                humidity = data['main']['humidity']
                weather_description = data['weather'][0]['description']
                self.icon_code = data['weather'][0]['icon']

                # Update label texts with weather information
                self.labelCity.text = f"{city_name}"
                self.labelTemp.text = f"{int(temperature)}°C"
                self.labelHumidity.text = f"{humidity}%"
                self.labelDescription.text = f"{weather_description.capitalize()}"
                
                Clock.schedule_once(lambda dt: self.calculate_icon_position(), 0) #Scheduled Calling the Calculation Function
           
        except requests.exceptions.Timeout:
            print("Weather update timed out. Skipping update.")
        except Exception as e:
            print("Error fetching weather:", e)
    def calculate_icon_position(self):
        # So these following Calculations return X position for the Icon.
        # I'm sure there will be a better and simple way but I choose this ugly method.
        text_width = len(self.labelDescription.text)
        adj_Calculation = 240 - text_width  
        xx_position = round((adj_Calculation/240) - (text_width/text_width), 1) + 0.265 # 0.265 is a sort of callibration value
        # Print statements
        # print(text_width)
        # print(adj_Calculation)
        print(xx_position)
        # Load and display the weather icon after calculating the position
        icon_path = f"icons/{self.icon_code}.png"
        weather_icon = Image(source=icon_path, pos_hint={'center_x': xx_position, 'center_y': 0.4}, size_hint=(0.08, 0.08))
        self.weather_icon = weather_icon  
        self.layout.add_widget(weather_icon)

    def orientation(self, *args):
        if accelerometer.get_x() > 0.3:
            Window.rotation=0
            #print("Rotating by 0")
        elif accelerometer.get_x() < -0.3 :
            Window.rotation=180
            #print("Rotating by 180")
        elif accelerometer.get_y() > 0.3 :
            Window.rotation=270
            #print("Rotating by 270")
        elif accelerometer.get_y() < -0.3 :
            Window.rotation=90
            #print("Rotating by 90")
    def brightness(self, *args):
        global count
        if button_a.is_pressed() == True:    
            count +=10
            os.system("brightness " + str(count))
            print(count)
        if button_b.is_pressed() == True: 
            count -=10
            os.system("brightness " + str(count))
            print(count)
            

if __name__ == '__main__':
    DigitalClock().run()
