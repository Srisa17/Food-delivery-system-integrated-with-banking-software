from tabulate import tabulate
import random
import time
from Bank import *

class Swiggy:
  def place_order():
    v='veg'
    nv='nonveg'
    menu = {"ptm": ("Paneer Tikka Masala", 230, "veg"), "vk": ("Veg. Kolhapuri", 220, "veg"), "gbs": ("Garlic Bread Sticks", 100, "veg"), 
            "vmp": ("Veg. Margherita Pizza", 99, "veg"), "psp": ("Pink Sauce Pasta", 120, "veg"), "cgb": ("Cheese Garlic Bread", 115, "veg"), 
            "atb": ("Aloo Tikki Burger", 45, "veg"), "clc": ("Choco Lava Cake", 45, "veg"), "cpo": ("Chicken Pepperoni and Onion", 199, "nonveg"), 
            "cp": ("Chicken Pasta", 250, "nonveg"), "cm": ("Chicken Momos", 125, "nonveg"), "cl": ("Chicken Lollipop", 85, "nonveg"),
            "c65": ("Chicken 65", 107, "nonveg"),"ck": ("Chicken Kebab", 250, "nonveg")
            }

    c=input("Do you want to see only the veg items in the menu?")
    if c.lower() == "yes" or c.lower()=="y":
      head = ["Code", "Item", 'Cost']
      print('Veg menu:')
      m = [(code, item, price) for code,(item, price, category) in menu.items() if category=='veg']
      print(tabulate(m, head, tablefmt="grid"))
    else:
      head = ["Type", "Item", "Code", 'Cost']
      vm = [(code, item, price, category) for code, (item, price, category) in menu.items() if category == "veg"]
      nm = [(code, item, price, category) for code, (item, price, category) in menu.items() if category == "nonveg"]
      print(tabulate(vm+nm, head, tablefmt="grid"))
    o=[]
    cost=0
    while True:
      x=input("Enter your order (Enter 'done' if completed ordering):").strip().lower()
      if x=='done':
        break
      if (x in menu and menu[x][2]==v):
          u=int(input("Enter no. of units: "))
          if u>0:
            cc= u*menu[x][1]
            cost+= cc
            o.append([x,u,menu[x][1],cc])
          else:
            print("Inavlid amount. Please try again.")
            continue
      elif x in menu and menu[x][2]==nv:
          u=int(input("Enter no. of units: "))
          if u>0:
            cc= u*menu[x][1]
            cost+= cc
            o.append([x,u,menu[x][1],cc])
          else:
            print("Inavlid amount. Please try again.")
            continue
    if o!=[]:
      o.append(["Total cost","","",cost])
      h=["Items ordered", "no. of units", "price per unit", "final cost"]
      print(f"Your order is:\n{tabulate(o,headers=h,tablefmt='grid')}")
      k=input("Do u want to proceed to payment:")
      if k.lower()=="n" or k.lower()=="no":
        confirm=input("Are you sure?")
        if confirm.lower()=="y" or confirm.lower()=="yes":
          del o
          print("Terminating.....")
          time.sleep(2)
          exit(0)
        if confirm.lower()=="n" or confirm.lower()=="no":
          k="y"
      if k.lower()=="y" or k.lower()=="yes":
        h=[]
        for uc in range(0,3):
          un=input("Enter username:")
          if Bank.authentication(un):
            if Bank.operation(4,un,"Swiggy",h,cost):
              print("Payment succesful")
              time.sleep(1.5)
              print("\nPrinting Receipt")
              time.sleep(1)
              print("\nReceipt:")
              head=["Username","Amount Paid"]
              md=[[str(un),str(cost)]]
              print(tabulate(md,headers=head,tablefmt="grid"))
              print(f"Your order will be delivered in {random.randint(10,45)} mins.\nHope u have a great day.")
              return True
            else:
              c=input("Payment Failed. Do you want to convert to COD?")
              if c.lower()=="y" or c.lower()=="yes":
                print(f"Your order will be delivered in {random.randint(10,45)} mins.\nHope u have a great day.")
              else:
                print("Your order cannot be placed. Thank you for using Swiggy.")
                exit(0)
            break
      else:
        print("Invalid input.")
        print("Terminating.....")
        time.sleep(2)
        exit(0)

  def __init__(self):
    print("Welcome to Swiggy!")
    Swiggy.place_order()

Swiggy()