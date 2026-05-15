import openpyxl as op
import customtkinter as ctk

NAME = "A"
QUANTITY = "B"
THRESHOLD = "C"

wb = op.load_workbook("inventory.xlsx") # Rows are numbers and columns are letters
sheet = wb.active

def get_index(row_num, col_letter):
    return col_letter + str(row_num)

def add_inventory():
    name = input("Name: ")
    if find_row(name) != False:
        print("This item has already been entered.")
        return
    quant = int(input("Quantity: "))
    row = find_row(None)
    n_index = get_index(row, "A")
    sheet[n_index].value = name
    q_index = get_index(row, QUANTITY)
    sheet[q_index].value = quant

def update_inventory():
    name = input("Name: ")
    row = find_row(name)
    if not row:
        print("Please enter a valid name.")
        return False
    index = get_index(row, QUANTITY)
    sign = input("Do you want to + OR -: ")
    quant_used = int(input("Enter the quanity used: "))
    if sign == "-":
        sheet[index].value -= quant_used
    elif sign == "+":
        sheet[index].value += quant_used
    else:
        print("Please enter a valid sign.")
        return False
    if sheet[index].value < sheet[get_index(row, THRESHOLD)].value:
        print(f"ALERT!!! Inventory for {name} is below Threshold, order more!")

def set_inventory():
    name = input("Name: ")
    row = find_row(name)
    if not row:
        print("Please enter a valid name.")
        return False
    index = get_index(row, QUANTITY)
    quant = int(input("Enter the value for quantity: "))
    sheet[index].value = quant

    if sheet[index].value < sheet[get_index(row, THRESHOLD)].value:
        print(f"ALERT!!! Inventory for {name} is below Threshold, order more!")

def find_row(val):
    i = 1
    while True:
        index = get_index(i, NAME)
        if sheet[index].value == val:
            return i
        elif sheet[index].value == None and val != None:
            return False
        i += 1

def alerts():
    i = 2
    while sheet[get_index(i, NAME)].value != None:
        if sheet[get_index(i, QUANTITY)].value < sheet[get_index(i, THRESHOLD)].value:
            print(f"Inventory for {sheet[get_index(i, NAME)].value} is too low!")
        i += 1

def main():
    while True:
        opt = input("Enter Option: Add Inventory(A), Update Inventory(U), Set Quantity Value(S), Exit(E), Alerts(L)").lower()
        if opt == "a":
            add_inventory()
            wb.save("inventory.xlsx")
        elif opt == "u":
            update_inventory()
            wb.save("inventory.xlsx")
        elif opt == "e":
            wb.save("inventory.xlsx")
            print("Inventory Saved")
            exit()
        elif opt == "s":
            set_inventory()
            wb.save("inventory.xlsx")
        elif opt == "l":
            alerts()
        else:
            print("Please choose a valid option.")

main()
