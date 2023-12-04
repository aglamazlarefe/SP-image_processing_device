from os import error, getcwd
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame


current_directory = getcwd()
print(current_directory)
frame_number= r"\frame3"
ASSETS_PATH = Path(current_directory + r"\Screens\Assets" + frame_number)   
print(ASSETS_PATH)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def optikread_clicked():
    try:
        frame.destroy()
        optik_read_frame = Frame(window)
        optik_read_frame.pack()

    except error:
        print(error)

def Writealignment_clicked():
    try:
        frame.destroy()
        write_alignment_frame = Frame(window)
        write_alignment_frame.pack()

    except error:
        print(error)

def sestanima_clicked():
    try:
        frame.destroy()
        yazılı_ses_tanıma_frame = Frame(window)
        yazılı_ses_tanıma_frame.pack()

    except error:
        print(error)



    






window = Tk()


#window.attributes('-fullscreen',True)
window.geometry("480x320")
window.configure(bg = "#47C4B6")


canvas = Canvas(
    window,
    bg = "#47C4B6",
    height = 320,
    width = 480,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=optikread_clicked,
    relief="flat"
)
















button_1.place(x=19.0,y=107.0,width=125.34329223632812,height=126.0)







button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
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
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=sestanima_clicked,
    relief="flat"
)
#button_3.place(x=x3, y=y, width=125.34326171875, height=button_height)
button_3.place(x=337.0,y=107.0,width=125.34326171875,height=126.0)

frame = Frame(window)
frame.pack()

window.resizable(False, False)
window.mainloop()