import customtkinter as ctk
import CTkTable as ctable
from PIL import Image
import openpyxl as op

app = ctk.CTk()
wb = op.load_workbook("inventory.xlsx", data_only=True) # Rows are numbers and columns are letters
sheet = wb.active
col_num_indexes = ["A", "B", "C", "D", "E", "F", "G"]

def get_index(row_num, col_letter):
    return col_letter + str(row_num)

def find_row(val):
    i = 1
    while True:
        index = get_index(i, "A")
        if sheet[index].value == val:
            return i
        elif sheet[index].value == None and val != None:
            return False
        i += 1

# Indexing Variables
team = None
category = None
item_search = None

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("system")
ctk.set_widget_scaling(1.5)

app.title("Inventory Tracker")
app.geometry("1200x800")

label = ctk.CTkLabel(app, text="CATalyst Inventory", fg_color="transparent", font=("Arial", 20, "bold"))
label.pack(pady=10)

def on_return(event):
    item_search = search.get()
    render_table(item_search, team, category)

search = ctk.CTkEntry(app, placeholder_text="Search for an item...")
search.pack(pady=10)
search.bind("<Return>", on_return)

def update_sub_menu(choice):
    global team
    # Data mapping categories to sub-items
    data = {
        "Fabrication": ["Filament", "Wood", "Acrylic", "Resin"],
        "Fiber Arts": ["Consumables", "Non-Consumables", "Machines/Parts"],
        "Multimedia": ["E-Cabinet", "Sound Studio", "VR", "Green Screen"],
        "Crafting": ["Screen Printing", "Roland", "Crafting Cabinets", "Buttons"]
    }

    team = choice
    sub_menu.configure(values=data[choice])
    sub_menu.set(data[choice][0])

main_menu = ctk.CTkOptionMenu(app, values=["Fabrication", "Fiber Arts", "Multimedia", "Crafting"], command=update_sub_menu, hover=True)
main_menu.set("Select Team")
main_menu.pack(pady=10, side=ctk.TOP)

def set_value(choice):
    global category, item_search
    category = choice
    item_search = None
    search.delete(0, "end")
    render_table(item_search, team, category)

sub_menu = ctk.CTkOptionMenu(app, values=["Select Team First"], command=set_value)
sub_menu.pack(pady=10)

# Table Code
table_frame = ctk.CTkScrollableFrame(app)
table_frame.pack(pady=10, padx=50, fill="both", expand=True)

# Error Label
error_label = ctk.CTkLabel(app, text="", text_color="red")
error_label.pack()

my_image = ctk.CTkImage(light_image=Image.open("edit.png"), size=(20, 20))
mode = 0 # 0 - Locked, 1 - Edit

value = [["Item", "Qty on Floor", "Qty in Back", "Par", "Qty to Order"],
            ["", "", "", "", ""],
            ["", "", "", "", ""]]
table = ctable.CTkTable(table_frame, row=1, column=5, values=value)
table.pack(padx=50, pady=20)

def update_board():
    global table
    global value
    for i in range(1, len(value)):
        for j in range(1, 3):
            row_num = find_row(value[i][0])
            sheet[get_index(row_num, col_num_indexes[j])].value = int(table.get_row(i)[j])
            sheet[get_index(row_num, col_num_indexes[4])].value = sheet[get_index(row_num, col_num_indexes[3])].value - sheet[get_index(row_num, col_num_indexes[1])].value - sheet[get_index(row_num, col_num_indexes[2])].value # Qty_O Calculation
            table.insert(i, 4, value=max(sheet[get_index(row_num, col_num_indexes[4])].value, 0))
            wb.save("inventory.xlsx")

def edit_button_clicked():
        global mode
        global value
        global table
        if mode == 0:
            table.configure(write=1)
            for i in range(1, len(value)):
                for j in range(1, 3):
                    table.edit(i, j, fg_color="green")
            edit_button.configure(text="Lock")
            mode = 1
        else:
            table.configure(write=0)
            edit_button.configure(text="Edit")
            update_board()
            mode = 0


edit_button = ctk.CTkButton(app, image=my_image, text="Edit", command=edit_button_clicked)
edit_button.pack(pady=10)

def render_table(item_search, team, category):
    global table
    global value
    global mode
    row_c = 0
    if item_search != None:
        i = 1
        while True:
            val = sheet[get_index(i, "A")].value
            if val == item_search:
                error_label.configure(text="")
                value = [["Item", "Qty on Floor", "Qty in Back", "Par", "Qty to Order"],
                         [sheet[get_index(i, "A")].value, sheet[get_index(i, "B")].value, sheet[get_index(i, "C")].value, sheet[get_index(i, "D")].value, max(int(sheet[get_index(i, "E")].value), 0)]]
                row_c = 1
                break
            elif val == None:
                error_label.configure(text=f"Item '{item_search}' not found.")
                break
            i += 1
    elif team != None and category != None:
        i = 1
        value = [["Item", "Qty on Floor", "Qty in Back", "Par", "Qty to Order"]]
        while True:
            if sheet[get_index(i, "F")].value == team and sheet[get_index(i, "G")].value == category:
                value.append([sheet[get_index(i, "A")].value, sheet[get_index(i, "B")].value, sheet[get_index(i, "C")].value, sheet[get_index(i, "D")].value, max(int(sheet[get_index(i, "E")].value), 0)])
                row_c += 1
            elif sheet[get_index(i, "A")].value == None:
                break
            i += 1

    # Put current data from table into excel before refresh
    if mode == 1:
        update_board()
        mode = 0
        edit_button.configure(text="Edit")

    table.destroy()
    table = ctable.CTkTable(table_frame, row=row_c+1, column=5, values=value)
    table.pack(pady=10, padx=50)

        

app.mainloop()


"""
TODO:
1. Display Error Message if user enters an invalid item name
3. Make the application scrollable, meaning that all the widgets don't shrink and instead the application becomes scrollable if the window is too small.
"""