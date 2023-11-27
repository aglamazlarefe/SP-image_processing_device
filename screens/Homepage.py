
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from logging import root
from os import error, getcwd
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,Frame


current_directory = getcwd()

frame_number= r"\frame3"
ASSETS_PATH =  Path(current_directory + r"\Screens\Assets" + frame_number)   

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)



def Writealignment_clicked():
    try:
        show_page(0)

        
        

    except error:
        print(error)

def optikread_clicked():
    try:
        show_page(0)

        

    except error:
        print(error)

def sestanima_clicked():
    try:
        show_page(0)

        

    except error:
        print(error)

def show_page(page):
    for p in pages:
        p.place_forget()
    pages[page].pack()



root= Tk()
window = Frame(root)

optik_read = Frame(window)
write_alignment = Frame(window)
yazil_ses_tanima = Frame(window)
pages = [window,optik_read,write_alignment, yazil_ses_tanima]




#window.attributes('-fullscreen',True)
root.geometry("480x320")
#root.configure(bg = "#47C4B6")



"""canvas = Canvas(
    window,
    bg = "#47C4B6",
    height = 320,
    width = 480,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)"""
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    window,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=optikread_clicked,
    relief="flat"
)




# Önce ekranın genişliğini alın
# Ekranın genişliğini ve yüksekliğini alın
"""screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Butonların toplam genişliği ve yüksekliği
total_button_width = (125.34329223632812 + 125.34326171875 + 125.34326171875)
button_height = 126.0

# Aralarında boşluk bırakmak için hesaplanmış ekstra boşluk
x_spacing = (screen_width - total_button_width) / 4
y_spacing = (screen_height - button_height) / 2

# Butonların ekranın ortasında olması için x ve y koordinatları
x1 = x_spacing
x2 = x1 + 125.34329223632812 + x_spacing
x3 = x2 + 125.34326171875 + x_spacing
y = y_spacing

# Butonları yerleştirin"""
#button_1.place(x=x1, y=y, width=125.34329223632812, height=button_height)

button_1.place(x=19.0,y=107.0,width=125.34329223632812,height=126.0)







button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    window,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=Writealignment_clicked,
    relief="flat"
)
#button_2.place(x=x2, y=y, width=125.34326171875, height=button_height)
button_2.place(x=179.0,y=107.0,width=125.34326171875,height=126.0)


button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    window,
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=sestanima_clicked,
    relief="flat"
)
#button_3.place(x=x3, y=y, width=125.34326171875, height=button_height)
button_3.place(x=337.0,y=107.0,width=125.34326171875,height=126.0)
show_page(0)

root.resizable(False, False)
root.mainloop()



