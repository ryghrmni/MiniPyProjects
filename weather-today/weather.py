import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

def get_weather(city):
    API_key = "b0ab593e36fa193be7c97364b5f53da8"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)
    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    weather= res.json()
    icon_id = weather['weather'][0]['icon']
    temp = weather['main']['temp'] - 273.15
    desc = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temp, desc, city, country)

def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    
    icon_url, temp, desc, city, country = result
    location_label.configure(text = f"{city}, {country}")

    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image = icon)
    icon_label.image = icon

    temp_label.configure(text = f"Temperature: {temp:.2f} C")
    description_label.configure(text = f"Description: {desc}")

root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("600x600")

city_entry = ttkbootstrap.Entry(root, font = "Helvetica, 18")
city_entry.pack(pady=10)

search_btn = ttkbootstrap.Button(root, text = "Search", command=search, bootstyle = "warning")
search_btn.pack(pady=10)

location_label = tk.Label(root, font="Helvetica 25")
location_label.pack(padx=20)

icon_label = tk.Label(root, font="Helvetica, 25")
icon_label.pack()

temp_label = tk.Label(root, font="Helvetica, 20")
temp_label.pack()

description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()