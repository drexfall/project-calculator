# setup.py
from distutils.core import setup
import py2exe
setup(windows=['main_app.py'],
      options = {
        'py2exe': {
            'packages': ['kivy','kivymd','PIL','qrcode']
        }
    })
