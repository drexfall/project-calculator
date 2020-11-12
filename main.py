from threading import Thread
import time
from kivy.utils import platform
def splash_func():
    import tkinter as tk
    import tkinter.ttk as ttk
    from PIL import Image, ImageTk

    class Splash(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            splash_size = int(self.winfo_screenwidth() /
                            4), int(self.winfo_screenheight()/4)
            self.geometry(f'{splash_size[0]*2}x{splash_size[1]*2}+{splash_size[0]}+{splash_size[1]}')

            self.splash_image = ImageTk.PhotoImage(Image.open('splash.jpg').resize((splash_size[0]*2, splash_size[1]*2)))
            tk.Label(self, image=self.splash_image).place(x=0, y=0)

            self.after(4000, self.destroy)
            self.overrideredirect(1)
    Splash().mainloop()
    
def main_func():
    time.sleep(1)
    from main_app import Main
    if platform!='android':
        t1.join()
        Main().run()
    
if platform!='android':
    t1 = Thread(target=splash_func)
    t2 = Thread(target=main_func)
    t1.start()
    t2.start()
else:
    main_func()