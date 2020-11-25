import json
import platform
from datetime import datetime
from urllib import error
from urllib.request import urlopen
from xml.etree.ElementTree import parse

from kivy.utils import platform as operating_system
from kivy.utils import rgba
from PIL import Image


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
    try:
        url = parse(urlopen("https://inr.fxexchangerate.com/rss.xml"))
        for item in url.iterfind("channel/item"):
            convert_unit_currency.append(str(item.findtext("title").split("/")[1]))
    except error.URLError as e:
        if "-2" in str(e.reason):
            convert_unit_currency.append("No Internet")
    convert_unit_currency.sort()

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


theme_image = {
    "theme1": ("text1", "hover1", "normal1", "pressed1", "Light"),
    "theme2": ("text2", "hover2", "normal2", "pressed2", "Light"),
    "theme3": ("text3", "hover3", "normal3", "pressed3", "Light"),
    "theme4": ("text4", "hover4", "normal4", "pressed4", "Light"),
    "theme5": ("text5", "hover5", "normal5", "pressed5", "Light"),
}
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
currency_unit_list()
current_page = [config_data["page_list"][0]["mode"]]
hover = [True]
font_color = theme_image[config_data["theme"]][0]
symbol = "-"
