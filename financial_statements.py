import pandas as pd
from datetime import datetime

class FinancialStatement:
    def __init__(self, ledger):
        self.ledger = ledger
        self.balances = ledger.get_account_balances()

class IncomeStatement(FinancialStatement):
    def __init__(self, ledger, start_date=None, end_date=None):
        super().__init__(ledger)
        self.start_date = start_date
        self.end_date = end_date
        self.revenue = 0
        self.expenses = 0
        self.net_income = 0
        self.calculate()

    def calculate(self):
        # Revenue accounts typically end with "Revenue" or "Income"
        revenue_accounts = [acc for acc in self.balances.keys() 
                          if acc.lower().endswith(('revenue', 'income', 'sales'))]
        self.revenue = sum(self.balances[acc] for acc in revenue_accounts)

        # Expense accounts typically end with "Expense" or "Cost"
        expense_accounts = [acc for acc in self.balances.keys() 
                          if acc.lower().endswith(('expense', 'cost'))]
        self.expenses = sum(self.balances[acc] for acc in expense_accounts)

        self.net_income = self.revenue - self.expenses

    def to_dataframe(self):
        return pd.DataFrame({
            'Category': ['Revenue', 'Expenses', 'Net Income'],
            'Amount': [self.revenue, self.expenses, self.net_income]
        })

class BalanceSheet(FinancialStatement):
    def __init__(self, ledger):
        super().__init__(ledger)
        self.assets = {}
        self.liabilities = {}
        self.equity = {}
        self.calculate()

    def calculate(self):
        # Asset accounts typically end with "Asset" or are specific asset types
        self.assets = {acc: bal for acc, bal in self.balances.items() 
                      if acc.lower().endswith(('asset', 'cash', 'receivable', 'inventory'))}

        # Liability accounts typically end with "Liability" or "Payable"
        self.liabilities = {acc: bal for acc, bal in self.balances.items() 
                          if acc.lower().endswith(('liability', 'payable', 'debt'))}

        # Equity accounts typically end with "Equity" or "Capital"
        self.equity = {acc: bal for acc, bal in self.balances.items() 
                      if acc.lower().endswith(('equity', 'capital', 'retained earnings'))}

    def to_dataframe(self):
        data = []
        # Add assets
        data.extend([{'Category': 'Assets', 'Account': acc, 'Amount': bal} 
                    for acc, bal in self.assets.items()])
        data.append({'Category': 'Assets', 'Account': 'Total Assets', 
                    'Amount': sum(self.assets.values())})
        
        # Add liabilities
        data.extend([{'Category': 'Liabilities', 'Account': acc, 'Amount': bal} 
                    for acc, bal in self.liabilities.items()])
        data.append({'Category': 'Liabilities', 'Account': 'Total Liabilities', 
                    'Amount': sum(self.liabilities.values())})
        
        # Add equity
        data.extend([{'Category': 'Equity', 'Account': acc, 'Amount': bal} 
                    for acc, bal in self.equity.items()])
        data.append({'Category': 'Equity', 'Account': 'Total Equity', 
                    'Amount': sum(self.equity.values())})
        
        return pd.DataFrame(data)

class StatementOfEquity(FinancialStatement):
    def __init__(self, ledger, start_date=None, end_date=None):
        super().__init__(ledger)
        self.start_date = start_date
        self.end_date = end_date
        self.beginning_equity = {}
        self.contributions = {}
        self.distributions = {}
        self.net_income = 0
        self.ending_equity = {}
        self.calculate()

    def calculate(self):
        # Get income statement for net income
        income_stmt = IncomeStatement(self.ledger, self.start_date, self.end_date)
        self.net_income = income_stmt.net_income

        # Equity accounts
        equity_accounts = [acc for acc in self.balances.keys() 
                         if acc.lower().endswith(('equity', 'capital', 'retained earnings'))]
        
        # Calculate changes in equity
        for account in equity_accounts:
            self.ending_equity[account] = self.balances[account]
            # This is a simplified calculation - in a real system, you'd track historical values
            self.beginning_equity[account] = 0
            self.contributions[account] = 0
            self.distributions[account] = 0

    def to_dataframe(self):
        data = []
        for account in self.ending_equity.keys():
            data.extend([
                {'Account': account, 'Category': 'Beginning Balance', 
                 'Amount': self.beginning_equity[account]},
                {'Account': account, 'Category': 'Contributions', 
                 'Amount': self.contributions[account]},
                {'Account': account, 'Category': 'Net Income', 
                 'Amount': self.net_income if 'retained earnings' in account.lower() else 0},
                {'Account': account, 'Category': 'Distributions', 
                 'Amount': self.distributions[account]},
                {'Account': account, 'Category': 'Ending Balance', 
                 'Amount': self.ending_equity[account]}
            ])
        return pd.DataFrame(data)

def export_to_excel(ledger, filename):
    """Export all financial statements to an Excel file."""
    with pd.ExcelWriter(filename) as writer:
        # Export Income Statement
        income_stmt = IncomeStatement(ledger)
        income_stmt.to_dataframe().to_excel(writer, sheet_name='Income Statement', index=False)
        
        # Export Balance Sheet
        balance_sheet = BalanceSheet(ledger)
        balance_sheet.to_dataframe().to_excel(writer, sheet_name='Balance Sheet', index=False)
        
        # Export Statement of Equity
        equity_stmt = StatementOfEquity(ledger)
        equity_stmt.to_dataframe().to_excel(writer, sheet_name='Statement of Equity', index=False)
        
        # Export General Ledger
        ledger_data = []
        for transaction in ledger.transactions:
            ledger_data.append({
                'Date': transaction.date,
                'Account': transaction.account,
                'Debit': transaction.debit,
                'Credit': transaction.credit,
                'Description': transaction.description
            })
        pd.DataFrame(ledger_data).to_excel(writer, sheet_name='General Ledger', index=False) 