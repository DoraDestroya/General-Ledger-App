import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from financial_statements import IncomeStatement, BalanceSheet, StatementOfEquity, export_to_excel

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

class LedgerApp:
    def __init__(self, master):
        self.master = master
        master.title("Accounting General Ledger")

        self.ledger = GeneralLedger()
        
        # Predefined accounts
        self.accounts = [
            "Cash",
            "Sales Revenue",
            "COGS",
            "Deferred Revenue",
            "Accounts Payable",
            "Accounts Receivable",
            "Interest Expense",
            "Interest Revenue",
            "Interest Payable"
        ]

        # Create notebook for tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Create tabs
        self.transactions_tab = ttk.Frame(self.notebook)
        self.statements_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.transactions_tab, text='Transactions')
        self.notebook.add(self.statements_tab, text='Financial Statements')

        # --- Transactions Tab ---
        self.setup_transactions_tab()
        
        # --- Financial Statements Tab ---
        self.setup_statements_tab()

    def setup_transactions_tab(self):
        # Input Section
        input_frame = ttk.LabelFrame(self.transactions_tab, text="Add Transaction")
        input_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(input_frame, text="Date:").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Account:").grid(row=1, column=0, padx=5, pady=5)
        self.account_var = tk.StringVar()
        self.account_dropdown = ttk.Combobox(input_frame, textvariable=self.account_var, values=self.accounts, state="readonly")
        self.account_dropdown.grid(row=1, column=1, padx=5, pady=5)
        self.account_dropdown.set(self.accounts[0])  # Set default value

        ttk.Label(input_frame, text="Debit:").grid(row=2, column=0, padx=5, pady=5)
        self.debit_entry = ttk.Entry(input_frame)
        self.debit_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Credit:").grid(row=3, column=0, padx=5, pady=5)
        self.credit_entry = ttk.Entry(input_frame)
        self.credit_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Description:").grid(row=4, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(input_frame)
        self.description_entry.grid(row=4, column=1, padx=5, pady=5)

        add_button = ttk.Button(input_frame, text="Add Transaction", command=self.add_transaction_ui)
        add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Ledger Display
        ledger_frame = ttk.LabelFrame(self.transactions_tab, text="General Ledger")
        ledger_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.ledger_tree = ttk.Treeview(ledger_frame, columns=("Date", "Account", "Debit", "Credit", "Description"))
        self.ledger_tree.heading("#1", text="Date")
        self.ledger_tree.heading("#2", text="Account")
        self.ledger_tree.heading("#3", text="Debit")
        self.ledger_tree.heading("#4", text="Credit")
        self.ledger_tree.heading("#5", text="Description")
        self.ledger_tree.pack(fill='both', expand=True, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.transactions_tab)
        button_frame.pack(fill='x', padx=5, pady=5)

        show_ledger_button = ttk.Button(button_frame, text="Show Ledger", command=self.update_ledger_display)
        show_ledger_button.pack(side='left', padx=5)

        show_t_accounts_button = ttk.Button(button_frame, text="Show T-Accounts", command=self.update_t_account_display)
        show_t_accounts_button.pack(side='left', padx=5)

        save_button = ttk.Button(button_frame, text="Save Ledger", command=self.save_ledger)
        save_button.pack(side='left', padx=5)

        load_button = ttk.Button(button_frame, text="Load Ledger", command=self.load_ledger)
        load_button.pack(side='left', padx=5)

        export_excel_button = ttk.Button(button_frame, text="Export to Excel", command=self.export_to_excel)
        export_excel_button.pack(side='left', padx=5)

    def setup_statements_tab(self):
        # Create frames for each statement
        income_frame = ttk.LabelFrame(self.statements_tab, text="Income Statement")
        income_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        balance_frame = ttk.LabelFrame(self.statements_tab, text="Balance Sheet")
        balance_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        equity_frame = ttk.LabelFrame(self.statements_tab, text="Statement of Equity")
        equity_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Income Statement
        self.income_tree = ttk.Treeview(income_frame, columns=("Category", "Amount"))
        self.income_tree.heading("#1", text="Category")
        self.income_tree.heading("#2", text="Amount")
        self.income_tree.pack(fill='both', expand=True, padx=5, pady=5)

        # Balance Sheet
        self.balance_tree = ttk.Treeview(balance_frame, columns=("Category", "Account", "Amount"))
        self.balance_tree.heading("#1", text="Category")
        self.balance_tree.heading("#2", text="Account")
        self.balance_tree.heading("#3", text="Amount")
        self.balance_tree.pack(fill='both', expand=True, padx=5, pady=5)

        # Statement of Equity
        self.equity_tree = ttk.Treeview(equity_frame, columns=("Account", "Category", "Amount"))
        self.equity_tree.heading("#1", text="Account")
        self.equity_tree.heading("#2", text="Category")
        self.equity_tree.heading("#3", text="Amount")
        self.equity_tree.pack(fill='both', expand=True, padx=5, pady=5)

        # Update button
        update_button = ttk.Button(self.statements_tab, text="Update Statements", 
                                 command=self.update_financial_statements)
        update_button.pack(pady=5)

    def add_transaction_ui(self):
        date = self.date_entry.get()
        account = self.account_var.get()  # Get selected account from dropdown
        debit_str = self.debit_entry.get()
        credit_str = self.credit_entry.get()
        description = self.description_entry.get()

        try:
            debit = float(debit_str) if debit_str else 0.0
            credit = float(credit_str) if credit_str else 0.0
            self.ledger.add_transaction(date, account, debit, credit, description)
            self.update_ledger_display()
            self.update_t_account_display()
            self.update_financial_statements()
            # Clear input fields after adding
            self.date_entry.delete(0, tk.END)
            self.account_dropdown.set(self.accounts[0])  # Reset dropdown to first account
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
            self.ledger_tree.insert("", tk.END, values=(
                transaction.date,
                transaction.account,
                f"{transaction.debit:.2f}",
                f"{transaction.credit:.2f}",
                transaction.description
            ))

    def update_t_account_display(self):
        t_accounts = self.ledger.generate_t_accounts()
        # Create a new window for T-accounts
        t_window = tk.Toplevel(self.master)
        t_window.title("T-Accounts")
        
        text = tk.Text(t_window, height=30, width=80)
        text.pack(padx=10, pady=10)
        
        for account, data in t_accounts.items():
            text.insert(tk.END, f"\n{'='*20} {account} {'='*20}\n")
            text.insert(tk.END, f"{'Debits':<15} | {'Credits':>15}\n")
            text.insert(tk.END, "-" * 31 + "\n")
            
            max_lines = max(len(data["debits"]), len(data["credits"]))
            for i in range(max_lines):
                debit = f"{data['debits'][i]:.2f}" if i < len(data["debits"]) else ""
                credit = f"{data['credits'][i]:.2f}" if i < len(data["credits"]) else ""
                text.insert(tk.END, f"{debit:<15} | {credit:>15}\n")
            
            text.insert(tk.END, "-" * 31 + "\n")
            text.insert(tk.END, f"{'Balance:':<15} | {data['balance']:>15.2f}\n")
        
        text.config(state='disabled')

    def update_financial_statements(self):
        # Update Income Statement
        for item in self.income_tree.get_children():
            self.income_tree.delete(item)
        income_stmt = IncomeStatement(self.ledger)
        for _, row in income_stmt.to_dataframe().iterrows():
            self.income_tree.insert("", tk.END, values=(row['Category'], f"${row['Amount']:.2f}"))

        # Update Balance Sheet
        for item in self.balance_tree.get_children():
            self.balance_tree.delete(item)
        balance_sheet = BalanceSheet(self.ledger)
        for _, row in balance_sheet.to_dataframe().iterrows():
            self.balance_tree.insert("", tk.END, values=(
                row['Category'],
                row['Account'],
                f"${row['Amount']:.2f}"
            ))

        # Update Statement of Equity
        for item in self.equity_tree.get_children():
            self.equity_tree.delete(item)
        equity_stmt = StatementOfEquity(self.ledger)
        for _, row in equity_stmt.to_dataframe().iterrows():
            self.equity_tree.insert("", tk.END, values=(
                row['Account'],
                row['Category'],
                f"${row['Amount']:.2f}"
            ))

    def save_ledger(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Date", "Account", "Debit", "Credit", "Description"])
                    for transaction in self.ledger.transactions:
                        writer.writerow([
                            transaction.date,
                            transaction.account,
                            transaction.debit,
                            transaction.credit,
                            transaction.description
                        ])
                messagebox.showinfo("Success", "Ledger saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving ledger: {e}")

    def load_ledger(self):
        filepath = filedialog.askopenfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filepath:
            try:
                self.ledger.transactions = []
                with open(filepath, 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader, None)  # Skip the header row
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
                self.update_financial_statements()
                messagebox.showinfo("Success", "Ledger loaded successfully!")
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading ledger: {e}")

    def export_to_excel(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filepath:
            try:
                export_to_excel(self.ledger, filepath)
                messagebox.showinfo("Success", "Financial statements exported to Excel successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting to Excel: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LedgerApp(root)
    root.mainloop()