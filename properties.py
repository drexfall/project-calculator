import json
import platform
from datetime import datetime
from urllib import error
from urllib.request import urlopen
from xml.etree.ElementTree import parse

from kivy.utils import platform as operating_system


def config_create():
    try:
        with open('config.json', 'r+') as config:
            global config_data
            config_data = json.load(config)

    except FileNotFoundError:
        with open('config.json', 'w+') as config:

            data = {
                "base": "e",
                "open_page": "standard",
                "history_length": 100,
                "inverse": 0,
                "radian": 0,
                "theme": "theme1",
                "typeface": "Century_Gothic",
                "page_list": ["standard",
                              "scientific",
                              "algebra",
                              "convert",
                              "days"
                              ]
            }
            json.dump(data, config, indent=4)
        config_create()


def write_history(exp, sol, mode):
    file = json.loads(open('history.json', 'r+').read())
    if len(file) > config_data["history_length"]:
        file.pop(list(file.keys())[0])
    file.update({str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))                 : ({exp: sol}, mode, platform.node()+'-'+operating_system+' device')})
    open('history.json', 'w').write(json.dumps(file, indent=4))


def light_mode():
    if operating_system == 'Windows':
        import winreg
        a = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        b = winreg.OpenKey(
            a, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
        c = winreg.QueryValueEx(b, 'AppsUseLightTheme')
        return bool(c[0])
    if operating_system == 'Android':
        pass


def currency_unit_list():
    global convert_unit_currency
    try:
        url = parse(urlopen('https://inr.fxexchangerate.com/rss.xml'))
        for item in url.iterfind('channel/item'):
            convert_unit_currency.append(
                str(item.findtext('title'))[-4:-1])
    except error.URLError as e:
        if '-2' in str(e.reason):
            print("No internet")

    convert_unit_currency.sort()


button_text_standard = ('Del',   'AC',
                        '÷',   '1',   '2',   '3',   '%',
                        'x',   '4',   '5',   '6',   'a²',
                        '+',   '7',   '8',   '9',   '√a',
                        '-',   '(',   '0',   ')',   'a!',
                        '.')

button_text_scientific = ('Del',  'AC',
                          'sin',   'cos',   'tan',   'cosec',   'sec',  'cot',
                          '÷',   '1',   '2',   '3',   'π',  'log',
                          'x',   '4',   '5',   '6',   'e',  'a²',
                          '+',   '7',   '8',   '9',   'a!',  '⌈a⌉',
                          '-',   '(',   '0',   ')',   '|a|',  '⌊a⌋',
                          '±',   '.',   '%')

button_text_scientific_inverse = ('INV',   'Rad',   'Del',  'AC',
                                  'sin¯',   'cos¯',   'tan¯',   'cosec¯',   'sec¯',  'cot¯',
                                  '÷',   '1',   '2',   '3',   'π',  'log',
                                  'x',   '4',   '5',   '6',   'e',  'a²',
                                  '+',   '7',   '8',   '9',   'a!',  '⌈a⌉',
                                  '-',   '(',   '0',   ')',   '|a|',  '⌊a⌋',
                                  '±',   '.',   '%')

button_text_convert = ('1',   '2',   '3',
                       '4',   '5',   '6',  'Del',
                       '7',   '8',   '9',  'AC',
                       '.',   '0',   'Go!'
                       )

convert_quantities = ('area',
                      'currency',
                      'energy',
                      'length',
                      'speed',
                      'temperature',
                      'time'
                      )

convert_unit_energy = ('joule',
                       'kilojoule',
                       'kilocalorie'
                       )

convert_unit_area = ('sqkm',
                     'sqcm',
                     'sqm',
                     'sqmm',
                     'sqft',
                     'sqin'
                     )

convert_unit_speed = ('m/s',
                      'km/hr',
                      'mph'
                      )

convert_unit_time = ('hr',
                     'min',
                     'sec',
                     'msec'
                     )
convert_unit_length = ('m',
                       'cm',
                       'km',
                       'nm',
                       'inch',
                       'foot',
                       'mm',
                       'mile'
                       )

convert_unit_temperature = ('cel',
                            'fhr',
                            'kel'
                            )

convert_unit_weight = ('kg',
                       'g',
                       'mg',
                       't',
                       'st',
                       'lb',
                       'oz',
                       'mg',
                       'ng',
                       )

theme_color = {'theme2':   ([0.98, 0.88, 0.90], [0.58, 0.9, 0.68], [0.40, 0.73, 0.58], [0.26, 0.24, 0.24]),
               'theme1':   ([0.00, 0.08, 0.15], [0.97, 0.09, 0.2], [0.71, 0.96, 0.93], [0.99, 1.00, 0.98]),
               'theme3':   ([0.00, 0.08, 0.15], [0.97, 0.09, 0.2], [0.71, 0.96, 0.93], [0.99, 1.00, 0.98]),
               'theme4':   ()}

convert_unit_currency = []
config_data = None
config_create()
currency_unit_list()
current_page = [config_data['page_list'][0]['mode']]
hover = [True]
font_color = theme_color[config_data['theme']][0]
