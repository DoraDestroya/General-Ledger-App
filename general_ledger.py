class Transaction:
    def __init__(self, date, account, debit, credit, description):
        self.date = date
        self.account = account
        self.debit = float(debit)
        self.credit = float(credit)
        self.description = description

class GeneralLedger:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, date, account, debit, credit, description):
        if debit >= 0 and credit >= 0 and debit != credit:  # Basic validation
            self.transactions.append(Transaction(date, account, debit, credit, description))
        else:
            print("Invalid transaction: Debits and credits must be non-negative and unequal.")

    def display_ledger(self):
        print("Date\t\tAccount\t\tDebit\t\tCredit\t\tDescription")
        print("-" * 80)
        for transaction in self.transactions:
            print(f"{transaction.date}\t{transaction.account}\t\t{transaction.debit:.2f}\t\t{transaction.credit:.2f}\t\t{transaction.description}")

    def get_account_balances(self):
        balances = {}
        for transaction in self.transactions:
            if transaction.account not in balances:
                balances[transaction.account] = 0
            balances[transaction.account] += transaction.debit - transaction.credit
        return balances

    def generate_t_accounts(self):
        t_accounts = {}
        for transaction in self.transactions:
            account = transaction.account
            debit = transaction.debit
            credit = transaction.credit

            if account not in t_accounts:
                t_accounts[account] = {"debits": [], "credits": [], "balance": 0}

            if debit > 0:
                t_accounts[account]["debits"].append(debit)
                t_accounts[account]["balance"] += debit
            elif credit > 0:
                t_accounts[account]["credits"].append(credit)
                t_accounts[account]["balance"] -= credit
        return t_accounts

    def display_t_accounts(self):
        t_accounts = self.generate_t_accounts()
        for account, data in t_accounts.items():
            print(f"\n{'='*20} {account} {'='*20}")
            print(f"{'Debits':<15} | {'Credits':>15}")
            print("-" * 31)
            max_lines = max(len(data["debits"]), len(data["credits"]))
            for i in range(max_lines):
                debit = f"{data['debits'][i]:.2f}" if i < len(data["debits"]) else ""
                credit = f"{data['credits'][i]:.2f}" if i < len(data["credits"]) else ""
                print(f"{debit:<15} | {credit:>15}")
            print("-" * 31)
            print(f"{'Balance:':<15} | {data['balance']:>15.2f}")

# Example Usage (with T-accounts)
ledger = GeneralLedger()
ledger.add_transaction("2025-05-06", "Cash", 1000.00, 0.00, "Initial investment")
ledger.add_transaction("2025-05-06", "Owner's Equity", 0.00, 1000.00, "Initial investment")
ledger.add_transaction("2025-05-07", "Supplies", 200.00, 0.00, "Purchased office supplies")
ledger.add_transaction("2025-05-07", "Cash", 0.00, 200.00, "Purchased office supplies")
ledger.add_transaction("2025-05-08", "Accounts Receivable", 500.00, 0.00, "Sales on credit")
ledger.add_transaction("2025-05-08", "Sales Revenue", 0.00, 500.00, "Sales on credit")
ledger.add_transaction("2025-05-09", "Cash", 300.00, 0.00, "Received cash from customer")
ledger.add_transaction("2025-05-09", "Accounts Receivable", 0.00, 300.00, "Received cash from customer")

ledger.display_ledger()
print("\nAccount Balances:")
balances = ledger.get_account_balances()
for account, balance in balances.items():
    print(f"{account}: ${balance:.2f}")

print("\nT-Accounts:")
ledger.display_t_accounts()
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv  # For saving/loading to CSV

class LedgerApp:
    def __init__(self, master):
        self.master = master
        master.title("Accounting General Ledger")

        self.ledger = GeneralLedger() # Assuming your GeneralLedger class

        # --- Input Section ---
        ttk.Label(master, text="Date:").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(master)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(master, text="Account:").grid(row=1, column=0, padx=5, pady=5)
        self.account_entry = ttk.Entry(master)
        self.account_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(master, text="Debit:").grid(row=2, column=0, padx=5, pady=5)
        self.debit_entry = ttk.Entry(master)
        self.debit_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(master, text="Credit:").grid(row=3, column=0, padx=5, pady=5)
        self.credit_entry = ttk.Entry(master)
        self.credit_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(master, text="Description:").grid(row=4, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(master)
        self.description_entry.grid(row=4, column=1, padx=5, pady=5)

        add_button = ttk.Button(master, text="Add Transaction", command=self.add_transaction_ui)
        add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # --- Ledger Display ---
        ttk.Label(master, text="\nGeneral Ledger:").grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.ledger_tree = ttk.Treeview(master, columns=("Date", "Account", "Debit", "Credit", "Description"))
        self.ledger_tree.heading("#1", text="Date")
        self.ledger_tree.heading("#2", text="Account")
        self.ledger_tree.heading("#3", text="Debit")
        self.ledger_tree.heading("#4", text="Credit")
        self.ledger_tree.heading("#5", text="Description")
        self.ledger_tree.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        # --- T-Account Display (Simplified - could be in a new window) ---
        ttk.Label(master, text="\nT-Accounts:").grid(row=8, column=0, columnspan=2, padx=5, pady=5)
        self.t_account_text = tk.Text(master, height=10, width=60)
        self.t_account_text.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        # --- Buttons for Actions ---
        show_ledger_button = ttk.Button(master, text="Show Ledger", command=self.update_ledger_display)
        show_ledger_button.grid(row=10, column=0, padx=5, pady=5)

        show_t_accounts_button = ttk.Button(master, text="Show T-Accounts", command=self.update_t_account_display)
        show_t_accounts_button.grid(row=10, column=1, padx=5, pady=5)

        save_button = ttk.Button(master, text="Save Ledger", command=self.save_ledger)
        save_button.grid(row=11, column=0, padx=5, pady=5)

        load_button = ttk.Button(master, text="Load Ledger", command=self.load_ledger)
        load_button.grid(row=11, column=1, padx=5, pady=5)

        self.update_ledger_display() # Initial display

    def add_transaction_ui(self):
        date = self.date_entry.get()
        account = self.account_entry.get()
        debit_str = self.debit_entry.get()
        credit_str = self.credit_entry.get()
        description = self.description_entry.get()

        try:
            debit = float(debit_str) if debit_str else 0.0
            credit = float(credit_str) if credit_str else 0.0
            self.ledger.add_transaction(date, account, debit, credit, description)
            self.update_ledger_display()
            self.update_t_account_display()
            # Clear input fields after adding
            self.date_entry.delete(0, tk.END)
            self.account_entry.delete(0, tk.END)
            self.debit_entry.delete(0, tk.END)
            self.credit_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid debit or credit amount.")

    def update_ledger_display(self):
        # Clear existing data in the treeview
        for item in self.ledger_tree.get_children():
            self.ledger_tree.delete(item)
        # Populate with current ledger data
        for transaction in self.ledger.transactions:
            self.ledger_tree.insert("", tk.END, values=(transaction.date, transaction.account, f"{transaction.debit:.2f}", f"{transaction.credit:.2f}", transaction.description))

    def update_t_account_display(self):
        self.t_account_text.delete("1.0", tk.END) # Clear previous text
        t_accounts = self.ledger.generate_t_accounts()
        output = ""
        for account, data in t_accounts.items():
            output += f"\n{'='*20} {account} {'='*20}\n"
            output += f"{'Debits':<15} | {'Credits':>15}\n"
            output += "-" * 31 + "\n"
            max_lines = max(len(data["debits"]), len(data["credits"]))
            for i in range(max_lines):
                debit = f"{data['debits'][i]:.2f}" if i < len(data["debits"]) else ""
                credit = f"{data['credits'][i]:.2f}" if i < len(data["credits"]) else ""
                output += f"{debit:<15} | {credit:>15}\n"
            output += "-" * 31 + "\n"
            output += f"{'Balance:':<15} | {data['balance']:>15.2f}\n"
        self.t_account_text.insert(tk.END, output)

    def save_ledger(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if filepath:
            try:
                with open(filepath, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Date", "Account", "Debit", "Credit", "Description"]) # Write header
                    for transaction in self.ledger.transactions:
                        writer.writerow([transaction.date, transaction.account, transaction.debit, transaction.credit, transaction.description])
                messagebox.showinfo("Success", "Ledger saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving ledger: {e}")

    def load_ledger(self):
        filepath = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if filepath:
            try:
                self.ledger.transactions = [] # Clear existing ledger
                with open(filepath, 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader, None) # Skip the header row
                    for row in reader:
                        if len(row) == 5:
                            date, account, debit, credit, description = row
                            try:
                                debit = float(debit)
                                credit = float(credit)
                                self.ledger.add_transaction(date, account, debit, credit, description)
                            except ValueError:
                                messagebox.showerror("Error", f"Invalid numeric data in CSV: {row}")
                self.update_ledger_display()
                self.update_t_account_display()
                messagebox.showinfo("Success", "Ledger loaded successfully!")
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading ledger: {e}")

root = tk.Tk()
app = LedgerApp(root)
root.mainloop()