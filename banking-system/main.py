import tkinter as tk
from tkinter import messagebox, simpledialog

class BankSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, name):
        if name not in self.accounts:
            self.accounts[name] = BankAccount(name)
            self.save_accounts()
            return True
        else:
            return False

    def delete_account(self, name):
        if name in self.accounts:
            del self.accounts[name]
            self.save_accounts()
            return True
        else:
            return False

    def rename_account(self, old_name, new_name):
        if old_name in self.accounts and new_name not in self.accounts:
            self.accounts[new_name] = self.accounts.pop(old_name)
            self.accounts[new_name].name = new_name
            self.save_accounts()
            return True
        else:
            return False

    def get_account(self, name):
        return self.accounts.get(name)

    def get_account_names(self):
        return list(self.accounts.keys())

    def load_accounts(self):
        try:
            with open("accounts.txt", "r") as file:
                for line in file:
                    name, balance = line.strip().split(":")
                    self.accounts[name] = BankAccount(name, float(balance))
        except FileNotFoundError:
            pass

    def save_accounts(self):
        with open("accounts.txt", "w") as file:
            for name, account in self.accounts.items():
                file.write(f"{name}:{account.balance}\n")

class BankAccount:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            messagebox.showinfo("Deposit", f"Deposited {amount} into {self.name}'s account.")
        else:
            messagebox.showerror("Error", "Invalid deposit amount.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            messagebox.showinfo("Withdrawal", f"Withdrew {amount} from {self.name}'s account.")
        else:
            messagebox.showerror("Error", "Insufficient funds.")

    def check_balance(self):
        messagebox.showinfo("Balance", f"{self.name}'s account balance: {self.balance}")

def deposit_action():
    try:
        amount = float(deposit_entry.get())
        account.deposit(amount)
        deposit_entry.delete(0, tk.END)  # Clear the entry field after deposit
        bank_system.save_accounts()  # Save updated account details
        enable_account_selection()  # Re-enable account selection after transaction
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")

def withdraw_action():
    try:
        amount = float(withdraw_entry.get())
        account.withdraw(amount)
        withdraw_entry.delete(0, tk.END)  # Clear the entry field after withdrawal
        bank_system.save_accounts()  # Save updated account details
        enable_account_selection()  # Re-enable account selection after transaction
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")

def balance_action():
    account.check_balance()
    enable_account_selection()  # Re-enable account selection after checking balance

def exit_action():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        window.destroy()

def create_account_action():
    name = name_entry.get()
    if bank_system.create_account(name):
        messagebox.showinfo("Account Created", f"Account for {name} created successfully.")
        name_entry.delete(0, tk.END)
        update_account_list()  # Update the account list after creating a new account
    else:
        messagebox.showerror("Error", "Account already exists.")

def select_account_action():
    selected_name = account_listbox.get(tk.ACTIVE)
    selected_account = bank_system.get_account(selected_name)
    if selected_account:
        global account
        account = selected_account
        name_entry.delete(0, tk.END)
        name_entry.insert(0, selected_name)
        name_entry.config(state='disabled')
        create_button.config(state='disabled')
        deposit_button.config(state='normal')
        withdraw_button.config(state='normal')
        balance_button.config(state='normal')
        exit_button.config(state='normal')
    else:
        messagebox.showerror("Error", "Account does not exist.")

def enable_account_selection():
    name_entry.config(state='normal')
    create_button.config(state='normal')
    deposit_button.config(state='disabled')
    withdraw_button.config(state='disabled')
    balance_button.config(state='disabled')
    exit_button.config(state='disabled')

def delete_account_action():
    selected_name = account_listbox.get(tk.ACTIVE)
    if selected_name:
        if account and selected_name == account.name:
            messagebox.showerror("Error", "Cannot delete the currently selected account.")
        else:
            confirmed = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the account '{selected_name}'?")
            if confirmed:
                if bank_system.delete_account(selected_name):
                    update_account_list()
                    messagebox.showinfo("Account Deleted", f"Account '{selected_name}' has been deleted.")
                else:
                    messagebox.showerror("Error", f"Account '{selected_name}' does not exist.")
    else:
        messagebox.showerror("Error", "Please select an account to delete.")

def rename_account_action():
    selected_name = account_listbox.get(tk.ACTIVE)
    if selected_name:
        new_name = simpledialog.askstring("Rename Account", "Enter the new name for the account:")
        if new_name:
            if bank_system.rename_account(selected_name, new_name):
                update_account_list()
                messagebox.showinfo("Account Renamed", f"Account '{selected_name}' has been renamed to '{new_name}'.")
            else:
                messagebox.showerror("Error", f"Failed to rename account. Either the account '{new_name}' already exists or '{selected_name}' does not exist.")
    else:
        messagebox.showerror("Error", "Please select an account to rename.")

bank_system = BankSystem()
account = None
window = None
name_entry = None
create_button = None
deposit_button = None
withdraw_button = None
balance_button = None
exit_button = None
deposit_entry = None
withdraw_entry = None
account_listbox = None

def main():
    global window, name_entry, create_button, deposit_button, withdraw_button, balance_button, exit_button, deposit_entry, withdraw_entry, account_listbox

    window = tk.Tk()
    window.title("Simple Banking System")

    welcome_label = tk.Label(window, text="Welcome to Simple Banking System!", font=("Helvetica", 16))
    welcome_label.grid(row=0, column=0, columnspan=2, pady=10)

    name_label = tk.Label(window, text="Enter your name:")
    name_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

    name_entry = tk.Entry(window)
    name_entry.grid(row=1, column=1, padx=10, pady=5)

    create_button = tk.Button(window, text="Create Account", command=create_account_action)
    create_button.grid(row=2, column=0, columnspan=2, pady=5)

    select_button = tk.Button(window, text="Select Account", command=select_account_action)
    select_button.grid(row=3, column=0, columnspan=2, pady=5)

    account_listbox = tk.Listbox(window)
    account_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    deposit_label = tk.Label(window, text="Deposit amount:")
    deposit_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
    deposit_entry = tk.Entry(window)
    deposit_entry.grid(row=5, column=1, padx=10, pady=5)
    deposit_button = tk.Button(window, text="Deposit", command=deposit_action, state='disabled')
    deposit_button.grid(row=6, column=0, columnspan=2, pady=5)

    withdraw_label = tk.Label(window, text="Withdraw amount:")
    withdraw_label.grid(row=7, column=0, padx=10, pady=5, sticky=tk.E)
    withdraw_entry = tk.Entry(window)
    withdraw_entry.grid(row=7, column=1, padx=10, pady=5)
    withdraw_button = tk.Button(window, text="Withdraw", command=withdraw_action, state='disabled')
    withdraw_button.grid(row=8, column=0, columnspan=2, pady=5)

    balance_button = tk.Button(window, text="Check Balance", command=balance_action, state='disabled')
    balance_button.grid(row=9, column=0, columnspan=2, pady=5)

    exit_button = tk.Button(window, text="Exit", command=exit_action, state='disabled')
    exit_button.grid(row=10, column=0, columnspan=2, pady=5)

    delete_button = tk.Button(window, text="Delete Account", command=delete_account_action)
    delete_button.grid(row=11, column=0, columnspan=2, pady=5)

    rename_button = tk.Button(window, text="Rename Account", command=rename_account_action)
    rename_button.grid(row=12, column=0, columnspan=2, pady=5)

    bank_system.load_accounts()  # Load account details from file
    update_account_list()

    window.mainloop()

def update_account_list():
    account_listbox.delete(0, tk.END)
    account_names = bank_system.get_account_names()
    for name in account_names:
        account_listbox.insert(tk.END, name)

if __name__ == "__main__":
    main()