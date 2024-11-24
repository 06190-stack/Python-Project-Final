import tkinter as tk
from tkinter import messagebox

class RateRecorder:
    def __init__(self):
        self.rates = {
            ("PKR", "USD"): 0.0036,
            ("USD", "PKR"): 280,
            ("PKR", "EUR"): 0.0032,
            ("EUR", "PKR"): 310
        }

    def get_rate(self, source_currency, target_currency):
        return self.rates.get((source_currency, target_currency), None)

    def update_rate(self, source_currency, target_currency, new_rate):
        self.rates[(source_currency, target_currency)] = new_rate
        return f"Rate updated: {source_currency} to {target_currency} = {new_rate}"

class HistoryRecorder:
    def __init__(self):
        self.history = []

    def record_history(self, amount, source_currency, target_currency, converted_amount):
        self.history.append({
            "amount": amount,
            "source_currency": source_currency,
            "target_currency": target_currency,
            "converted_amount": converted_amount
        })

    def get_history(self):
        if not self.history:
            return "No history available."
        history_str = "Transaction History:\n"
        for record in self.history:
            history_str += f"{record['amount']} {record['source_currency']} -> {record['converted_amount']} {record['target_currency']}\n"
        return history_str

class CurrencyConverterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Currency Converter")
        self.rate_recorder = RateRecorder()
        self.history_recorder = HistoryRecorder()
        self.create_widgets()

    def create_widgets(self):
        """Set up the GUI widgets."""
        # Title Label
        tk.Label(self.root, text="Currency Converter", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        # Amount Input
        tk.Label(self.root, text="Amount:").grid(row=1, column=0, sticky="e", padx=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1, padx=5)

        # Source Currency
        tk.Label(self.root, text="Source Currency:").grid(row=2, column=0, sticky="e", padx=5)
        self.source_currency_entry = tk.Entry(self.root)
        self.source_currency_entry.grid(row=2, column=1, padx=5)

        # Target Currency
        tk.Label(self.root, text="Target Currency:").grid(row=3, column=0, sticky="e", padx=5)
        self.target_currency_entry = tk.Entry(self.root)
        self.target_currency_entry.grid(row=3, column=1, padx=5)

        # Convert Button
        tk.Button(self.root, text="Convert", command=self.convert_currency).grid(row=4, column=0, columnspan=2, pady=10)

        # Conversion Result
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.grid(row=5, column=0, columnspan=2, pady=10)

        # History Button
        tk.Button(self.root, text="View History", command=self.show_history).grid(row=6, column=0, columnspan=2, pady=5)

        # Update Rates Button
        tk.Button(self.root, text="Update Rates", command=self.update_rate).grid(row=7, column=0, columnspan=2, pady=5)

    def convert_currency(self):
        """Handle the currency conversion."""
        try:
            amount = float(self.amount_entry.get())
            source_currency = self.source_currency_entry.get().upper()
            target_currency = self.target_currency_entry.get().upper()

            rate = self.rate_recorder.get_rate(source_currency, target_currency)
            if rate is None:
                messagebox.showerror("Error", f"No conversion rate for {source_currency} to {target_currency}.")
                return

            converted_amount = amount * rate
            self.result_label.config(text=f"{amount} {source_currency} = {converted_amount:.2f} {target_currency}")
            self.history_recorder.record_history(amount, source_currency, target_currency, converted_amount)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def show_history(self):
        """Show the transaction history."""
        history = self.history_recorder.get_history()
        messagebox.showinfo("Transaction History", history)

    def update_rate(self):
        """Allow the user to update conversion rates."""
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Conversion Rates")

        tk.Label(update_window, text="Source Currency:").grid(row=0, column=0, sticky="e", padx=5)
        source_currency_entry = tk.Entry(update_window)
        source_currency_entry.grid(row=0, column=1, padx=5)

        tk.Label(update_window, text="Target Currency:").grid(row=1, column=0, sticky="e", padx=5)
        target_currency_entry = tk.Entry(update_window)
        target_currency_entry.grid(row=1, column=1, padx=5)

        tk.Label(update_window, text="New Rate:").grid(row=2, column=0, sticky="e", padx=5)
        new_rate_entry = tk.Entry(update_window)
        new_rate_entry.grid(row=2, column=1, padx=5)

        def save_rate():
            source = source_currency_entry.get().upper()
            target = target_currency_entry.get().upper()
            try:
                new_rate = float(new_rate_entry.get())
                message = self.rate_recorder.update_rate(source, target, new_rate)
                messagebox.showinfo("Success", message)
                update_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid rate.")

        tk.Button(update_window, text="Save", command=save_rate).grid(row=3, column=0, columnspan=2, pady=10)

    def run(self):
        """Run the main application loop."""
        self.root.mainloop()

if __name__ == "__main__":
    app = CurrencyConverterApp()
    app.run()