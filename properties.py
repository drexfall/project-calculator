import json
from os import mkdir
import platform
from datetime import datetime
from urllib import error
from urllib.request import urlopen
from xml.etree.ElementTree import parse

from kivy.utils import platform as operating_system
from kivy.utils import rgba
from PIL import Image

try:
    open("history.json", 'r')
except FileNotFoundError:
    with open("history.json", "w+") as file:
        file.write("{}")
with open("currency.json", "wb+") as file:
    response = urlopen("https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json")
    file.write(response.read())


def days_number(fdate, tdate):
    return abs(
        (
            datetime.strptime(fdate, config_data["format"])
            - datetime.strptime(tdate, config_data["format"])
        ).days
    )


def config_create():
    with open("config.json", "r+") as config:
        global config_data
        config_data = json.load(config)


def write_history(exp, sol, mode):
    file = json.loads(open("history.json", "r+").read())
    if len(file) > config_data["history_length"]:
        file.pop(list(file.keys())[0])
    file.update(
        {
            str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")): (
                {exp: sol},
                mode,
                platform.node() + "-" + operating_system + " device",
            )
        }
    )
    open("history.json", "w").write(json.dumps(file, indent=4))


def light_mode():
    if operating_system == "Windows":
        import winreg

        a = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        b = winreg.OpenKey(
            a, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        c = winreg.QueryValueEx(b, "AppsUseLightTheme")
        return bool(c[0])
    if operating_system == "Android":
        pass


def color(file):
    colors = Image.open(file).getpixel((0, 0))
    return rgba(colors)


def currency_unit_list():
    global convert_unit_currency
    with open("currency.json", "r") as jsonFile:
        try:
            data = json.load(jsonFile)
        except json.JSONDecodeError:
            print("Could not decode JSON")
            data = {}
    convert_unit_currency = data


convert_quantities = (
    "area",
    "currency",
    "energy",
    "length",
    "speed",
    "temperature",
    "time",
)

convert_unit_energy = ("joule", "kilojoule", "kilocalorie")

convert_unit_area = ("sqkm", "sqcm", "sqm", "sqmm", "sqft", "sqin")

convert_unit_speed = ("m/s", "km/hr", "mph")

convert_unit_time = ("hr", "min", "sec", "msec")
convert_unit_length = ("m", "cm", "km", "nm", "inch", "foot", "mm", "mile")

convert_unit_temperature = ("cel", "fhr", "kel")

convert_unit_weight = (
    "kg",
    "g",
    "mg",
    "t",
    "st",
    "lb",
    "oz",
    "mg",
    "ng",
)

theme_image = {}

formats = ("%d-%m-%y",
           "%d-%m-%Y",
           "%m-%d-%y",
           "%m-%d-%Y",
           "%m/%d/%Y",
           "%m/%d/%y",
           "%d/%m/%Y",
           "%d/%m/%y",
           "%m/%d/%Y",
           "%d-%a-%Y",
           "%d-%a-%y")
convert_unit_currency = []
config_data = None
config_create()

for index_x,x in enumerate(config_data["theme_colors"]):
    theme_image.update({x[0]: ([x[1], x[2], x[3], x[4]])})

    for index, y in enumerate(['text', 'hover', 'normal', 'pressed']):
        try:
            mkdir('images')
        except FileExistsError:
            pass
        Image.new('RGB', (50, 50), color=tuple(x[index+1])).save(f"images\\{y}{index_x+1}.png")
        theme_image[x[0]][index] = f"{y}{index_x+1}"

currency_unit_list()
current_page = [config_data["page_list"][0]["mode"]]
hover = [True]
font_color = theme_image[config_data["theme"]][0]
symbol = "-"
