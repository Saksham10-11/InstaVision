from pathlib import Path
from tkinter import Tk, Canvas, Entry,Button, PhotoImage
from handeler import handelInputCommands


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")

def handleExit():
    window.destroy()

def handleSearch():
    dirPath = entry_1.get()
    searchParam = entry_2.get()
    handelInputCommands(dirPath,searchParam)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("700x550")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 550,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.05960166337899864,
    50.09027099609375,
    250.15063096536323,
    550.1357856470859,
    fill="#ECF7F7",
    outline="")

canvas.create_rectangle(
    0.10967637466353608,
    0.09027099609375,
    700.1096763755195,
    50.09027100807634,
    fill="#1F47D3",
    outline="")

canvas.create_text(
    59.10967637490319,
    14.09027099609375,
    anchor="nw",
    text="VidPic Organiser",
    fill="#FFFFFF",
    font=("MarkoOne Regular", 22 * -1)
)

canvas.create_rectangle(
    250.10967636696057,
    50.09027099609375,
    700.1096763755195,
    550.0902710037968,
    fill="#FFFFFF",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=handleExit,
    relief="flat"
)
button_1.place(
    x=637.9999855619471,
    y=4.0,
    width=51.31808466711621,
    height=42.02534843892215
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    33.00001646169221,
    27.0,
    image=image_image_1
)

canvas.create_text(
    20.999996199241764,
    79.0,
    anchor="nw",
    text="Path :",
    fill="#000000",
    font=("MarkoOne Regular", 16 * -1)
)

canvas.create_text(
    20.999996199241764,
    160.0,
    anchor="nw",
    text="Find :",
    fill="#000000",
    font=("MarkoOne Regular", 16 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    125.99999619948147,
    123.00000000179739,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#DBD5D5",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=30.99999619922471,
    y=108.0,
    width=190.00000000051352,
    height=28.000000003594778
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    125.99999619948147,
    204.0000000017974,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#DBD5D5",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=30.99999619922471,
    y=189.0,
    width=190.00000000051352,
    height=28.000000003594778
)

canvas.create_rectangle(
    273.9999961922748,
    95.0,
    674.9999961997382,
    531.0000000068643,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    273.9999961991391,
    60.0,
    anchor="nw",
    text="Camera :",
    fill="#000000",
    font=("MarkoOne Regular", 22 * -1)
)

canvas.create_rectangle(
    273.99999619225775,
    94.0,
    674.9999961997382,
    531.0000000068643,
    fill="#000000",
    outline="")

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    472.999996192292,
    311.0,
    image=image_image_2
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=36.99050536196455,
    y=262.9529113769531,
    width=164.01895677005496,
    height=33.094200182708505
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=handleSearch,
    relief="flat"
)
button_3.place(
    x=36.99050536196455,
    y=262.9529113769531,
    width=164.01895677005496,
    height=33.094200182708505
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    120.99997575266889,
    441.0,
    image=image_image_3
)

canvas.create_rectangle(
    250.49999619973823,
    53.99547779451677,
    251.49999621075222,
    550.0046310424805,
    fill="#000000",
    outline="")
window.resizable(False, False)
window.mainloop()
