import customtkinter as ctk
import CTkTable as ctable
from PIL import Image

app = ctk.CTk()

# Indexing Variables
team = None
category = None
item_search = None

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("system")
ctk.set_widget_scaling(1.5)

app.title("Inventory Tracker")
app.geometry("600x400")

label = ctk.CTkLabel(app, text="CATalyst Inventory", fg_color="transparent", font=("Arial", 20, "bold"))
label.pack(pady=10)

def on_return(event):
    print(search.get())

search = ctk.CTkEntry(app, placeholder_text="Search for an item...")
search.pack(pady=10)
search.bind("<Return>", on_return)

def update_sub_menu(choice):
    # Data mapping categories to sub-items
    data = {
        "Fabrication": ["Filment", "Wood", "Acrylic", "Resin"],
        "Fiber Arts": ["Consumables", "Non-Consumables", "Machines/Parts"],
        "Multimedia": ["E-Cabinet", "Sound Studio", "VR", "Green Screen"],
        "Crafting": ["Screen Printing", "Roland", "Crafting Cabinets", "Buttons"]
    }

    sub_menu.configure(values=data[choice])
    sub_menu.set(data[choice][0])

main_menu = ctk.CTkOptionMenu(app, values=["Fabrication", "Fiber Arts", "Multimedia", "Crafting"], command=update_sub_menu, hover=True)
main_menu.set("Select Team")
main_menu.pack(pady=10, side=ctk.TOP)

def set_value(choice):
    category = choice

sub_menu = ctk.CTkOptionMenu(app, values=["Select Team First"], command=set_value)
sub_menu.pack(pady=10)

# Table Code
my_image = ctk.CTkImage(light_image=Image.open("edit.png"), size=(20, 20))
mode = 0 # 0 - Locked, 1 - Edit
def edit_button_clicked():
    global mode
    if mode == 0:
        table.configure(write=1)
        edit_button.configure(text="Lock")
        mode = 1
    else:
        table.configure(write=0)
        edit_button.configure(text="Edit")
        mode = 0

edit_button = ctk.CTkButton(app, image=my_image, text="Edit", command=edit_button_clicked)

value = [["Item", "Qty on Floor", "Qty in Back", "Par", "Qty to Order"],
         [1, 2, 25, 30],
         [2, "Bob", 30, 5]]

table = ctable.CTkTable(app, row=3, column=4, values=value)
table.pack(padx=50, pady=20)
edit_button.pack(pady=10)


app.mainloop()
