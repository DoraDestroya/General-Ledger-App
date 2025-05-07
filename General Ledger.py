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