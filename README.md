# General Ledger Application-William Macey Arkansas Accounting Student

A Python-based general ledger application with a graphical user interface that allows users to manage accounting transactions, view T-accounts, and maintain a general ledger. Made for Arkansas AI foundry Hackathon. Used Cursor to code and create the interface.
Created for small business owners to have a free General Ledger that can export to financial statements.
Used Python

## Features

- Add and manage accounting transactions
- View transactions in a general ledger format
- Generate and display T-accounts
- Save and load ledger data in CSV format
- User-friendly GUI interface

## Download

You can download the latest version of the application from the [Releases](https://github.com/DoraDestroya/General-Ledger-App/releases) page.

### System Requirements
- macOS 10.13 or later
- Windows 10 or later
- Linux (Ubuntu 20.04 or later)

## Development Setup

If you want to run the application from source:

1. Clone this repository:
```bash
git clone https://github.com/DoraDestroya/General-Ledger-App.git
cd General-Ledger-App
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python general_ledger.py
```

### Building from Source

To create your own executable:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller general_ledger.spec
```

The executable will be created in the `dist` directory.

## Usage

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
