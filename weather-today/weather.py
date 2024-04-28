# imports the required libraries
import tkinter as tk
import requests
from tkinter import messagebox
import ttkbootstrap
from PIL import Image, ImageTk
import regex as re
import calendar
import tkintermapview

# gets the weather status in the next 24 hours
def get_fullday():
    fdlabel_list = [fd1_label, fd2_label, fd3_label, fd4_label, fd5_label, fd6_label, fd7_label, fd8_label]
    fdicon_list = [fd1_image, fd2_image, fd3_image, fd4_image, fd5_image, fd6_image, fd7_image, fd8_image]
    fdtemp_list = [fd1_temp, fd2_temp, fd3_temp, fd4_temp, fd5_temp, fd6_temp, fd7_temp, fd8_temp]
    for i in range(8):
        # sets the text for time labels
        date_time = fc["list"][i]["dt_txt"]
        time = re.findall("\d.:00", date_time)[0]
        fdlabel_list[i].configure(text=time)
        # sets the icon for image labels
        icon_id = fc["list"][i]["weather"][0]["icon"]
        icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
        image = Image.open(requests.get(icon_url, stream= True).raw)
        image = image.resize((70, 70))
        icon = ImageTk.PhotoImage(image)
        fdicon_list[i].configure(image=icon)
        fdicon_list[i].image = icon
        # sets the temperature for temp labels
        temp = int(fc["list"][i]["main"]["temp"] - 273.15)
        fdtemp_list[i].configure(text=f"{temp}°")

# gets the name of the days 
def get_name(t):
    dlabel_list = [d1_label, d2_label, d3_label, d4_label]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hday = 8
    # gets every day's date using the dt_txt variable
    for i in range(4):
        date_time = fc["list"][hday]["dt_txt"]
        date = date_time.split()[0].split("-")
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        # gets the day as a number ( from 0 to 6 ) using calendar
        daynumber = calendar.weekday(year, month, day)
        dlabel_list[i].configure(text=days[daynumber])
        hday += 8

# gets today's weather status
def get_today(t):
    today_label.configure(text="Today")
    tempminlist = []
    tempmaxlist = []
    iconlist = []
    # gets every hour's maximum and minimum temp and icon
    for i in range(t):
        tempminlist.append(int(fc["list"][i]["main"]["temp_min"] - 273.15))
        tempmaxlist.append(int(fc["list"][i]["main"]["temp_max"] - 273.15))
        iconlist.append(fc["list"][i]["weather"][0]["icon"])

    minl = min(tempminlist)
    maxl = max(tempmaxlist)
    icon_id = max(set(iconlist), key=iconlist.count)
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    image = Image.open(requests.get(icon_url, stream= True).raw)
    image = image.resize((50, 50))
    icon = ImageTk.PhotoImage(image)
    # configs the labels
    today_image.configure(image=icon)
    today_image.image = icon
    todaymin_label.configure(text=f"{minl}°")
    todaymax_label.configure(text=f"{maxl}°")

# gets the next 4 days weather status
def get_future(t):
    hours = 8
    diconlist = [d1_image, d2_image, d3_image, d4_image]
    dminlist = [d1min_label, d2min_label, d3min_label, d4min_label]
    dmaxlist = [d1max_label, d2max_label, d3max_label, d4max_label]
    iconl = []
    tempminl = []
    tempmaxl = []
    # gets the next 4 days maximum and minimum temp and icon
    for x in range(4):
        for y in range(hours):
            tempminl.append(int(fc["list"][y+t]["main"]["temp_min"] - 273.15))
            tempmaxl.append(int(fc["list"][y+t]["main"]["temp_max"] - 273.15))
            iconl.append(fc["list"][y+t]["weather"][0]["icon"])

        minl = min(tempminl)
        maxl = max(tempmaxl)
        dminlist[x].configure(text=f"{minl}°")
        dmaxlist[x].configure(text=f"{maxl}°")

        icon_id = max(set(iconl), key=iconl.count)
        icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
        image = Image.open(requests.get(icon_url, stream= True).raw)
        image = image.resize((50, 50))
        icon = ImageTk.PhotoImage(image)
        diconlist[x].configure(image=icon)
        diconlist[x].image = icon
        # reset the variable for thee next day
        tempminl = []
        tempmaxl = []
        iconl = []
        t += 8

# gets the required information about the weather
def get_weather(city):
    global fc
    # connects to the api
    API_key = "b0ab593e36fa193be7c97364b5f53da8"
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(URL)
    if res.status_code == 404:
        messagebox.show_error("Error", "City Not Found")
        return None
    weather = res.json()
    lon = weather["coord"]["lon"]
    lat = weather["coord"]["lat"]
    resfc = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}")
    fc = resfc.json()
    icon_id = weather["weather"][0]["icon"]
    temperature =int(weather["main"]["temp"] - 273.15)
    description = weather["weather"][0]["description"].capitalize()
    city = weather["name"]
    countrty = weather["sys"]["country"]
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"

    # checks how many 3 hours are left today
    tdate = fc["list"][0]["dt_txt"].split()[0]
    todayh = 0
    h = 0
    running = True
    while running:
        todayh += 1
        h += 1
        date = fc["list"][h]["dt_txt"].split()[0]
        if date != tdate:
            running = False

    # calls the functions
    get_fullday()
    get_today(todayh)
    get_name(todayh)
    get_future(todayh)

    # returns the required variables
    return (icon_url, description, city, countrty, temperature, lon, lat)

# configs the labels at the top and calls the get_weather fnuction
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return ""

    icon_url, description, city, countrty, temperature, lon, lat = result
    location_label.configure(text=f"{city}, {countrty}")
    image = Image.open(requests.get(icon_url, stream= True).raw)
    image = image.resize((90, 90))
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon
    temperature_label.configure(text = f"{temperature}° C")
    description_label.configure(text = description)

    map_widget = tkintermapview.TkinterMapView(root, width=500, height=500, corner_radius=0)
    map_widget.set_position(lat, lon)
    map_widget.set_zoom(15)
    map_widget.place(x=650, y=125)

# defines the screen
root = ttkbootstrap.Window()
root.title("Weather Application")
root.geometry("1175x650")
root.resizable(False, False)

# defines the gui
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle='warning')
location_label = tk.Label(root, font="Helvetica, 25")
icon_label = tk.Label(root, font="Helvetica, 20")
description_label = tk.Label(root, text="", font="Helvetica, 20")
temperature_label = tk.Label(root, text="", font="Helvetica, 25")
fd1_label = tk.Label(root, font="Helvetica, 17")
fd2_label = tk.Label(root, font="Helvetica, 17")
fd3_label = tk.Label(root, font="Helvetica, 17")
fd4_label = tk.Label(root, font="Helvetica, 17")
fd5_label = tk.Label(root, font="Helvetica, 17")
fd6_label = tk.Label(root, font="Helvetica, 17")
fd7_label = tk.Label(root, font="Helvetica, 17")
fd8_label = tk.Label(root, font="Helvetica, 17")
fd1_image = tk.Label(root, font="Helvetica")
fd2_image = tk.Label(root, font="Helvetica")
fd3_image = tk.Label(root, font="Helvetica")
fd4_image = tk.Label(root, font="Helvetica")
fd5_image = tk.Label(root, font="Helvetica")
fd6_image = tk.Label(root, font="Helvetica")
fd7_image = tk.Label(root, font="Helvetica")
fd8_image = tk.Label(root, font="Helvetica")
fd1_temp = tk.Label(root, font="Helvetica, 17")
fd2_temp = tk.Label(root, font="Helvetica, 17")
fd3_temp = tk.Label(root, font="Helvetica, 17")
fd4_temp = tk.Label(root, font="Helvetica, 17")
fd5_temp = tk.Label(root, font="Helvetica, 17")
fd6_temp = tk.Label(root, font="Helvetica, 17")
fd7_temp = tk.Label(root, font="Helvetica, 17")
fd8_temp = tk.Label(root, font="Helvetica, 17")
today_label = tk.Label(root, font="Helvetica, 17")
d1_label = tk.Label(root, font="Helvetica, 17")
d2_label = tk.Label(root, font="Helvetica, 17")
d3_label = tk.Label(root, font="Helvetica, 17")
d4_label = tk.Label(root, font="Helvetica, 17")
today_image = tk.Label(root, font="Helvetica")
d1_image = tk.Label(root, font="Helvetica")
d2_image = tk.Label(root, font="Helvetica")
d3_image = tk.Label(root, font="Helvetica")
d4_image = tk.Label(root, font="Helvetica")
todaymin_label = tk.Label(root, font="Helvetica, 17")
d1min_label = tk.Label(root, font="Helvetica, 17")
d2min_label = tk.Label(root, font="Helvetica, 17")
d3min_label = tk.Label(root, font="Helvetica, 17")
d4min_label = tk.Label(root, font="Helvetica, 17")
todaymax_label = tk.Label(root, font="Helvetica, 17")
d1max_label = tk.Label(root, font="Helvetica, 17")
d2max_label = tk.Label(root, font="Helvetica, 17")
d3max_label = tk.Label(root, font="Helvetica, 17")
d4max_label = tk.Label(root, font="Helvetica, 17")

city_entry.pack(pady=10)
search_button.pack(pady=10)
location_label.place(x=5, y=100)
icon_label.place(x=-10, y=135)
description_label.place(x=80, y=165)
temperature_label.place(x=5, y=210)
fd1_label.place(x=0, y=280)
fd2_label.place(x=75, y=280)
fd3_label.place(x=150, y=280)
fd4_label.place(x=225, y=280)
fd5_label.place(x=300, y=280)
fd6_label.place(x=375, y=280)
fd7_label.place(x=450, y=280)
fd8_label.place(x=525, y=280)
fd1_image.place(x=-5, y=305)
fd2_image.place(x=70, y=305)
fd3_image.place(x=145, y=305)
fd4_image.place(x=220, y=305)
fd5_image.place(x=295, y=305)
fd6_image.place(x=370, y=305)
fd7_image.place(x=445, y=305)
fd8_image.place(x=520, y=305)
fd1_temp.place(x=15, y=370)
fd2_temp.place(x=90, y=370)
fd3_temp.place(x=165, y=370)
fd4_temp.place(x=240, y=370)
fd5_temp.place(x=315, y=370)
fd6_temp.place(x=390, y=370)
fd7_temp.place(x=465, y=370)
fd8_temp.place(x=540, y=370)
today_label.place(x=10, y=440)
d1_label.place(x=10, y=480)
d2_label.place(x=10, y=520)
d3_label.place(x=10, y=560)
d4_label.place(x=10, y=600)
todaymin_label.place(x=550, y=440)
d1min_label.place(x=550, y=480)
d2min_label.place(x=550, y=520)
d3min_label.place(x=550, y=560)
d4min_label.place(x=550, y=600)
todaymax_label.place(x=500, y=440)
d1max_label.place(x=500, y=480)
d2max_label.place(x=500, y=520)
d3max_label.place(x=500, y=560)
d4max_label.place(x=500, y=600)
today_image.place(x=445, y=430)
d1_image.place(x=445, y=470)
d2_image.place(x=445, y=510)
d3_image.place(x=445, y=550)
d4_image.place(x=445, y=590)

root.mainloop()