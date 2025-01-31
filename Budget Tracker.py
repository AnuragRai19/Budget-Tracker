import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
from datetime import datetime
import os

class BudgetTrackerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Personal Budget Tracker")
        master.geometry("400x500")

        # Transaction Listbox
        self.transaction_listbox = tk.Listbox(master, width=50, height=15)
        self.transaction_listbox.pack(pady=10)

        # Buttons Frame
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=10)

        # Create Buttons
        buttons = [
            ("Add Income", self.add_income),
            ("Add Expense", self.add_expense),
            ("View Balance", self.view_balance),
            ("Category Summary", self.category_summary)
        ]

        for (text, command) in buttons:
            tk.Button(btn_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)

        # Balance Label
        self.balance_var = tk.StringVar()
        self.balance_label = tk.Label(master, textvariable=self.balance_var, font=('Arial', 14))
        self.balance_label.pack(pady=10)

        # Initialize data file and load transactions
        self.filename = 'budget_data.csv'
        self.ensure_file_exists()
        self.load_transactions()
        self.update_balance()

    def ensure_file_exists(self):
        """Create budget file if it doesn't exist."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Category', 'Amount', 'Type'])

    def add_transaction(self, category, amount, transaction_type):
        """Add a transaction to the CSV and update UI."""
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            date = datetime.now().strftime('%Y-%m-%d')
            writer.writerow([date, category, round(float(amount), 2), transaction_type])
        
        # Reload transactions and update balance
        self.load_transactions()
        self.update_balance()

    def add_income(self):
        """Dialog to add income transaction."""
        category = simpledialog.askstring("Income", "Income Category:")
        if category:
            amount = simpledialog.askfloat("Income", "Amount:")
            if amount:
                self.add_transaction(category, amount, 'Income')

    def add_expense(self):
        """Dialog to add expense transaction."""
        category = simpledialog.askstring("Expense", "Expense Category:")
        if category:
            amount = simpledialog.askfloat("Expense", "Amount:")
            if amount:
                self.add_transaction(category, amount, 'Expense')

    def load_transactions(self):
        """Load transactions into listbox."""
        self.transaction_listbox.delete(0, tk.END)
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                display_text = f"{row[0]} | {row[1]} | ${row[2]} | {row[3]}"
                self.transaction_listbox.insert(tk.END, display_text)

    def update_balance(self):
        """Calculate and display total balance."""
        income = expenses = 0
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                amount = float(row['Amount'])
                if row['Type'] == 'Income':
                    income += amount
                else:
                    expenses += amount
        
        balance = round(income - expenses, 2)
        self.balance_var.set(f"Current Balance: ${balance}")

    def view_balance(self):
        """Show balance in a message box."""
        balance = self.balance_var.get()
        messagebox.showinfo("Balance", balance)

    def category_summary(self):
        """Show expense category summary."""
        category_totals = {}
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Type'] == 'Expense':
                    category = row['Category']
                    amount = float(row['Amount'])
                    category_totals[category] = category_totals.get(category, 0) + amount
        
        summary = "\n".join([f"{cat}: ${round(total, 2)}" for cat, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)])
        messagebox.showinfo("Expense Categories", summary)

def main():
    root = tk.Tk()
    app = BudgetTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()