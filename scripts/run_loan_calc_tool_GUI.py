import tkinter as tk
from tkinter import ttk, messagebox
from loan_calc_tool_class import Loan

class LoanCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Loan Calculator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Configure style
        style = ttk.Style()
        style.theme_use("clam")

        # Create main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Loan Calculator",
                                font=('Helvetica', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0,20))

        # Input fields
        ttk.Label(main_frame, text="Loan Amount ($):", font=('Helvetica', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.principal_var = tk.StringVar(value="300000")
        ttk.Entry(main_frame, textvariable=self.principal_var, width=20).grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        ttk.Label(main_frame, text="Annual Interest Rate (%)", font=('Helvetica', 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.rate_var = tk.StringVar(value="6.5")
        ttk.Entry(main_frame, textvariable=self.rate_var, width=20).grid(
            row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        ttk.Label(main_frame, text="Loan  Term (Years):", font=('Helvetica', 10)).grid(
            row=3, column=0, sticky=tk.W, pady=5)
        self.term_var = tk.StringVar(value="30")
        ttk.Entry(main_frame, textvariable=self.term_var, width=20).grid(
            row=3, column=1, sticky=(tk.W,tk.E), pady=5)

        # Calculate button
        calc_button = ttk.Button(main_frame, text="Calculate", command=self.calculate)
        calc_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Result frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        results_frame.columnconfigure(1, weight=1)

        ttk.Label(results_frame, text="Monthly Payment:", font=('Helvetica', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.monthly_payment_label = ttk.Label(results_frame, text="$0.00",
                                               font=('Helvetica', 10), foreground="green")
        self.monthly_payment_label.grid(row=0, column=1, sticky=tk.W, pady=5, padx=10)

        ttk.Label(results_frame, text="Total Payment:", font=('Helvetica', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.total_payment_label = ttk.Label(results_frame, text="$0.00",
                                             font=('Helvetica', 10))
        self.total_payment_label.grid(row=1, column=1, sticky=tk.W, pady=5, padx=10)

        ttk.Label(results_frame, text="Total Interest:", font=('Helvetica', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.total_interest_label = ttk.Label(results_frame, text="$0.00",
                                              font=('Helvetica', 10), foreground="red")
        self.total_interest_label.grid(row=2, column=1, sticky=tk.W, pady=5, padx=10)

        # Amortization schedule button
        schedule_button = ttk.Button(main_frame, text="View Amortization Schedule",
                                     command=self.show_schedule)
        schedule_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.loan = None

    def calculate(self):
        try:
            principal = float(self.principal_var.get())
            annual_rate = float(self.rate_var.get()) / 100
            term_years = float(self.term_var.get())
            term_months = int(term_years * 12)

            if principal <= 0 or annual_rate < 0 or term_months <= 0:
                raise ValueError("Please enter positive values")

            self.loan = Loan(principal, annual_rate, term_months)

            monthly = self.loan.monthly_payment()
            total = self.loan.total_payment()
            interest = self.loan.total_interest()

            self.monthly_payment_label.config(text=f"${monthly:,.2f}")
            self.total_payment_label.config(text=f"${total:,.2f}")
            self.total_interest_label.config(text=f"${interest:,.2f}")

        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid numeric values")
    def show_schedule(self):
        if self.loan is None:
            messagebox.showwarning("No Calculation", "Please calculate a loan first")
            return

        # Create new window
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Amortization Schedule")
        schedule_window.geometry("900x500")

        # Create treeview with scrollbar
        frame = ttk.Frame(schedule_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)


        tree = ttk.Treeview(frame, columns=('Month', 'Payment', 'Principal', 'Interest', 'Balance'),
                            show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)

        # Pack scrollbar and tree
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Define headings
        tree.heading('Month', text='Month')
        tree.heading('Payment', text='Payment')
        tree.heading('Principal', text='Principal')
        tree.heading('Interest', text='Interest')
        tree.heading('Balance', text='Balance')

        # Define column findings
        tree.column('Month', width=100, minwidth=80, anchor=tk.CENTER, stretch=False)
        tree.column('Payment', width=150, minwidth=120, anchor=tk.E, stretch=True)
        tree.column('Principal', width=150, minwidth=120, anchor=tk.E, stretch=True)
        tree.column('Interest', width=150, minwidth=120, anchor=tk.E, stretch=True)
        tree.column('Balance', width=150, minwidth=120, anchor=tk.E, stretch=True)

        # Insert data
        schedule = self.loan.amortization_schedule()
        for payment in schedule:
            tree.insert('', tk.END, values=(
                payment['month'],
                f"${payment['payment']:,.2f}",
                f"${payment['principal']:,.2f}"
                f"${payment['interest']:,.2f}",
                f"${payment['balance']:,.2f}"
            ))

        # Add info label
        info_label = ttk.Label(schedule_window,
                               text=f"Showingall {len(schedule)} payments",
                               font=('Helvetica', 9))
        info_label.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoanCalculatorGUI(root)
    root.mainloop()


