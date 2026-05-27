# Dependancy: psycopg2, doesn't come with sqlalchemy
import sqlalchemy as sqa
import sqlalchemy.orm as sqa_orm
import customtkinter as ctk
import CTkTable as ctable
from PIL import Image

app = ctk.CTk()

# Indexing Variables
team = None
category = None
item_search = None
col_num_indexes = ["A", "B", "C", "D", "E", "F", "G"]
inventory_items = []

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("system")
ctk.set_widget_scaling(1.5)

app.title("Inventory Tracker")
app.geometry("1200x800")

# Database Setup
DATABASE_URL = "postgresql://postgres:mathpanda@localhost:5432/CATalyst Inventory"

class Base(sqa_orm.DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "inventory"
    __table__ = sqa.Table("inventory", Base.metadata, autoload_with=sqa.create_engine(DATABASE_URL))

engine = sqa.create_engine(DATABASE_URL)

with sqa_orm.Session(engine) as session:
    inventory_items = session.query(User).all()
    for row in inventory_items:
        print(row.item, row.qty_f, row.qty_b, row.qty_o, row.par)


def find_row(val):
    global inventory_items
    c = 0

    for i in inventory_items:
        if i.item == val:
            return c
        c += 1
    return None


label = ctk.CTkLabel(app, text="CATalyst Inventory", fg_color="transparent", font=("Arial", 20, "bold"))
label.pack(pady=10)

def on_return(event):
    global item_search
    val = search.get().strip()
    item_search = val if val != "" else None
    render_table(item_search, team, category)

search = ctk.CTkEntry(app, placeholder_text="Search for an item...")
search.pack(pady=10)
search.bind("<Return>", on_return)

def update_sub_menu(choice):
    global team, category, item_search
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
    category = data[choice][0]
    item_search = None
    search.delete(0, "end")
    render_table(item_search, team, category)

main_menu = ctk.CTkOptionMenu(app, values=["Fabrication", "Fiber Arts", "Multimedia", "Crafting"], command=update_sub_menu, hover=True)
main_menu.set("Select Team")
main_menu.pack(pady=10, side=ctk.TOP)

def set_search_value(choice):
    global category, item_search
    category = choice
    item_search = None
    search.delete(0, "end")
    render_table(item_search, team, category)

sub_menu = ctk.CTkOptionMenu(app, values=["Select Team First"], command=set_search_value)
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
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "]]
table = ctable.CTkTable(table_frame, row=1, column=5, values=value)
table.pack(padx=50, pady=20)

def update_board():
    with sqa_orm.Session(engine) as session:
        for i in range(1, len(value)):
            item_name = value[i][0]
            row_num = find_row(item_name)
            if row_num is None:
                continue
 
            new_qty_f = int(table.get_row(i)[1])
            new_qty_b = int(table.get_row(i)[2])
            new_qty_o = inventory_items[row_num].par - (new_qty_f + new_qty_b)
 
            inventory_items[row_num].qty_f = new_qty_f
            inventory_items[row_num].qty_b = new_qty_b
            inventory_items[row_num].qty_o = new_qty_o
 
            qty_to_order = max(new_qty_o, 0)
            table.insert(i, 4, value=qty_to_order)
 
            # Persist to database
            db_item = session.query(User).filter(User.item == item_name).first()
            if db_item:
                db_item.qty_f = new_qty_f
                db_item.qty_b = new_qty_b
                db_item.qty_o = new_qty_o
 
        session.commit()

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
    global table, value, mode
    row_c = 0
 
    if item_search is not None:
        matched = None
        for item in inventory_items:
            if item.item == item_search:
                matched = item
                break
 
        if matched is None:
            error_label.configure(text=f"Item '{item_search}' not found.")
            return
 
        error_label.configure(text="")
        par = matched.par if matched.par is not None else 0
        qty_o = matched.qty_o if matched.qty_o is not None else 0
        qty_to_order = max(par - qty_o, 0)
        value = [
            ["Item", "Qty on Floor", "Qty in Back", "Par", "Qty to Order"],
            [matched.item, matched.qty_f, matched.qty_b, par, qty_to_order]
        ]
        row_c = 1
 
    elif team is not None and category is not None:
        value = [["Item", "Qty on Floor", "Qty in Back", "Par", "Qty to Order"]]
        for item in inventory_items:
            if item.team == team and item.category == category:
                par = item.par if item.par is not None else 0
                qty_o = item.qty_o if item.qty_o is not None else 0
                qty_to_order = max(par - qty_o, 0)
                value.append([item.item, item.qty_f, item.qty_b, par, qty_to_order])
                row_c += 1

    # Put current data from table into excel before refresh
    if mode == 1:
        update_board()
        mode = 0
        edit_button.configure(text="Edit")

    table.destroy()
    table = ctable.CTkTable(table_frame, row=row_c+1, column=5, values=value)
    table.pack(pady=10, padx=50)

        

app.mainloop()
