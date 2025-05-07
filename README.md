# General Ledger Application

A Python-based general ledger application with a graphical user interface that allows users to manage accounting transactions, view T-accounts, and maintain a general ledger.

## Features

- Add and manage accounting transactions
- View transactions in a general ledger format
- Generate and display T-accounts
- Save and load ledger data in CSV format
- User-friendly GUI interface

## Requirements

- Python 3.x
- tkinter (usually comes with Python)
- csv (built-in Python module)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/general-ledger.git
cd general-ledger
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python general_ledger.py
```

### Adding Transactions
1. Enter the transaction details in the input fields:
   - Date
   - Account
   - Debit amount
   - Credit amount
   - Description
2. Click "Add Transaction" to record the transaction

### Viewing Data
- Use "Show Ledger" to view all transactions
- Use "Show T-Accounts" to view T-account format
- Save/Load functionality available for data persistence

## License

This project is licensed under the MIT License - see the LICENSE file for details.