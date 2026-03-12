import re
import sqlite3
from tabulate import tabulate
from getpass import getpass

# --- DATABASE SETUP ---
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# Create Tables
cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS accounts (username TEXT PRIMARY KEY, balance REAL)')
cursor.execute('CREATE TABLE IF NOT EXISTS beneficiaries (username TEXT, beneficiary_name TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS vendors (vendor_name TEXT PRIMARY KEY)')

# Default Data Injection (using IGNORE to prevent duplicates on rerun)
initial_users = [("Jane", "Abcdefgh#1"), ("Alice", "Alpha#0011"), ("Swiggy", "Zomato#12")]
initial_balances = [("Jane", 1000.3), ("Alice", 123.332), ("Swiggy", 1239094.324)]
initial_bens = [("Jane", "Alice"), ("Alice", "Jane")]
initial_vendors = [("Swiggy",)]

cursor.executemany('INSERT OR IGNORE INTO users VALUES (?,?)', initial_users)
cursor.executemany('INSERT OR IGNORE INTO accounts VALUES (?,?)', initial_balances)
cursor.executemany('INSERT OR IGNORE INTO beneficiaries VALUES (?,?)', initial_bens)
cursor.executemany('INSERT OR IGNORE INTO vendors VALUES (?)', initial_vendors)
conn.commit()

class Bank:
    def authentication(u):
        cursor.execute('SELECT password FROM users WHERE username=?', (u,))
        res = cursor.fetchone()
        if res:
            db_password = res[0]
            for i in range(3):
                p = getpass("Enter password:")
                if db_password == p:
                    print('Authentication successful')
                    return True
                else:
                    print("Incorrect Password")
            print("Maximum tries exceeded. Terminating.")
            return False
        
        c = input("User does not exist. Do you want to sign up?\n")
        if c.lower() in ["yes", "y"]:
            Bank.signup(u)
        else:
            print("Thank You")
            return False

    def Password(u):
        while True:
            p = getpass("Input Password: ")
            p1, p2, p3, p4 = r"[^a-zA-Z0-9]", r"[^a-z0-9\s]", r"[^a-zA-Z\s]", r"[^A-Z0-9\s]"
            
            rules = [
                len(p) >= 8,
                p != u,
                re.search(p1, p),
                re.search(p2, p),
                re.search(p3, p),
                re.search(p4, p)
            ]
            
            if all(rules):
                return p
            else:
                print("Not a valid password\nTry again")

    def signup(u):
        cursor.execute('SELECT username FROM users WHERE username=?', (u,))
        while cursor.fetchone():
            u = input("Username already exists, please try a different one: ")
            cursor.execute('SELECT username FROM users WHERE username=?', (u,))
            
        p = Bank.Password(u)
        cursor.execute('INSERT INTO users VALUES (?,?)', (u, p))
        cursor.execute('INSERT INTO accounts VALUES (?,?)', (u, 0.0))
        conn.commit()
        print(f"User {u} created.")

    def Transaction(uname):
        if Bank.authentication(uname):
            hist = []
            v = 0.0
            while True:
                o = int(input("\n1. Withdrawal\n2. Deposit\n3. Transfer\n4. Merchant\n5. Statement\n0. Back\nChoice:"))
                if o == 0 or o > 5:
                    C = input("Are you sure you want to go back?")
                    if C.lower() in ["y", "yes"]: return True
                elif o < 3:
                    Bank.operation(o, uname, uname, hist, v)
                elif o >= 3:
                    u = input("Enter Username of the receiver/merchant:")
                    Bank.operation(o, uname, u, hist, v)

    def operation(o, uname, uid, hist, a):
        # Fetch current balance helper
        def get_bal(name):
            cursor.execute('SELECT balance FROM accounts WHERE username=?', (name,))
            res = cursor.fetchone()
            return res[0] if res else None

        current_bal = get_bal(uname)

        if o == 1:
            a = float(input("Enter amount to withdraw:"))
            if a > current_bal: print("Insufficient balance")
            elif a < 0: print("Invalid amount")
            else:
                cursor.execute('UPDATE accounts SET balance = balance - ? WHERE username = ?', (a, uname))
                hist.append(-a)
        
        elif o == 2:
            a = float(input("Enter amount to deposit:"))
            cursor.execute('UPDATE accounts SET balance = balance + ? WHERE username = ?', (a, uname))
            hist.append(a)

        elif o == 3:
            cursor.execute('SELECT 1 FROM beneficiaries WHERE username=? AND beneficiary_name=?', (uname, uid))
            if cursor.fetchone():
                a = float(input("Enter amount to transfer:"))
                if 0 < a <= current_bal:
                    cursor.execute('UPDATE accounts SET balance = balance + ? WHERE username = ?', (a, uid))
                    cursor.execute('UPDATE accounts SET balance = balance - ? WHERE username = ?', (a, uname))
                    hist.append(a)
                else: print("Transaction failed: Check balance.")
            else:
                if input("Beneficiary not found. Add? (y/n)").lower() == 'y':
                    cursor.execute('INSERT INTO beneficiaries VALUES (?,?)', (uname, uid))
        
        elif o == 4:
            cursor.execute('SELECT 1 FROM vendors WHERE vendor_name=?', (uid,))
            if cursor.fetchone():
                a = float(input("Enter amount for merchant:"))
                if 0 < a <= current_bal:
                    cursor.execute('UPDATE accounts SET balance = balance + ? WHERE username = ?', (a, uid))
                    cursor.execute('UPDATE accounts SET balance = balance - ? WHERE username = ?', (a, uname))
                    hist.append(a)
                    print("Payment Successful")
            else: print("Merchant not found.")

        conn.commit()
        # History and Balance display
        new_bal = get_bal(uname)
        md = [[str(uname), str(new_bal)]]
        print("\nBalance\n", tabulate(md, headers=["Username", "Balance"], tablefmt="grid"))

    def delete(uname):
        if Bank.authentication(uname):
            cursor.execute('DELETE FROM users WHERE username=?', (uname,))
            cursor.execute('DELETE FROM accounts WHERE username=?', (uname,))
            cursor.execute('DELETE FROM beneficiaries WHERE username=?', (uname,))
            conn.commit()
            print("Account Deletion successful")

    def choice(c):
        if c == 1:
            uname = input("Enter Username:")
            Bank.signup(uname)
        elif c == 2:
            uname = input("Enter Username:")
            if Bank.authentication(uname):
                while True:
                    o = int(input("\n1. Transaction\n2. Balance\n3. Delete\n0. Logout\nChoice: "))
                    if o == 0 or o > 3: break
                    if o == 1: Bank.Transaction(uname)
                    elif o == 2:
                        cursor.execute('SELECT balance FROM accounts WHERE username=?', (uname,))
                        bal = cursor.fetchone()[0]
                        print(tabulate([[uname, bal]], headers=["User", "Balance"], tablefmt="grid"))
                    elif o == 3: 
                        Bank.delete(uname)
                        break
        else:
            conn.close()
            exit(0)

    def __init__(self):
        while True:
            try:
                c = int(input("\n1. Signup\n2. Login\n3. Exit\nEnter choice: "))
                Bank.choice(c)
            except ValueError: print("Enter a valid number.")

if __name__ == "__main__":
    Bank()