"""
Desktop GUI application for Cash Up using tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
from cash_up_core import CashUpCalculator, ReportGenerator
from config import Config

class CashUpDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cash Up Application")
        self.root.geometry("800x600")
        self.root.configure(bg='#0d1117')
        
        # Configure dark theme colors
        self.colors = {
            'bg_primary': '#0d1117',
            'bg_secondary': '#161b22',
            'bg_tertiary': '#21262d',
            'text_primary': '#f0f6fc',
            'text_secondary': '#8b949e',
            'terminal_green': '#00ff00',
            'terminal_amber': '#ffb000',
            'accent_red': '#f85149',
            'accent_blue': '#58a6ff',
            'border': '#30363d'
        }
        
        # Initialize core components
        self.calculator = CashUpCalculator({
            'DEFAULT_FLOAT': Config.DEFAULT_FLOAT
        })
        self.report_generator = ReportGenerator(Config.REPORTS_DIR)
        
        # Initialize variables
        self.cash_counts = [tk.IntVar() for _ in range(len(self.calculator.denominations))]
        self.receipt_amounts = []
        self.additional_cash_entries = []
        self.expected_takings_var = tk.DoubleVar()
        self.date_var = tk.StringVar()
        
        # Set today's date
        self.date_var.set(datetime.now().strftime("%d/%m/%Y"))
        
        self.create_widgets()
        self.update_totals()
    
    def create_widgets(self):
        # Configure ttk styles for dark theme
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme styles
        style.configure('Dark.TFrame', background=self.colors['bg_primary'])
        style.configure('Dark.TLabel', background=self.colors['bg_primary'], foreground=self.colors['text_primary'])
        style.configure('Dark.TLabelFrame', background=self.colors['bg_primary'], foreground=self.colors['text_primary'])
        style.configure('Dark.TLabelFrame.Label', background=self.colors['bg_primary'], foreground=self.colors['terminal_green'])
        style.configure('Dark.TEntry', fieldbackground=self.colors['bg_tertiary'], foreground=self.colors['text_primary'], borderwidth=1)
        style.configure('Dark.TButton', background=self.colors['terminal_green'], foreground=self.colors['bg_primary'])
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10", style='Dark.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Cash Up Application", 
                               font=('Monaco', 16, 'bold'), style='Dark.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Date entry
        ttk.Label(main_frame, text="Date:", style='Dark.TLabel').grid(row=1, column=0, sticky=tk.W, pady=2)
        date_entry = ttk.Entry(main_frame, textvariable=self.date_var, width=15, style='Dark.TEntry')
        date_entry.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # Cash counts section
        cash_frame = ttk.LabelFrame(main_frame, text="Cash Count", padding="10", style='Dark.TLabelFrame')
        cash_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        cash_frame.columnconfigure(1, weight=1)
        
        self.cash_entries = []
        for i, denom in enumerate(self.calculator.denominations):
            row = i // 3
            col = (i % 3) * 2
            
            ttk.Label(cash_frame, text=f"{denom}:", style='Dark.TLabel').grid(row=row, column=col, sticky=tk.W, padx=(0, 5))
            entry = ttk.Entry(cash_frame, textvariable=self.cash_counts[i], width=8, style='Dark.TEntry')
            entry.grid(row=row, column=col+1, sticky=tk.W, padx=(0, 20))
            entry.bind('<KeyRelease>', lambda e: self.update_totals())
            entry.bind('<KeyPress>', lambda e, idx=i: self.handle_cash_input_keys(e, idx))
            self.cash_entries.append(entry)
        
        # Cash total
        self.cash_total_label = ttk.Label(cash_frame, text="Total Cash: £0.00", 
                                         font=('Monaco', 10, 'bold'), style='Dark.TLabel')
        self.cash_total_label.grid(row=len(self.calculator.denominations)//3 + 1, 
                                  column=0, columnspan=6, pady=(10, 0))
        
        # Help text
        help_label = ttk.Label(cash_frame, text="Tip: Use SPACE for +10, ↓ for -10, ←→ for ±1", 
                              font=('Monaco', 8), foreground=self.colors['terminal_amber'])
        help_label.grid(row=len(self.calculator.denominations)//3 + 2, 
                       column=0, columnspan=6, pady=(5, 0))
        
        # Receipts section
        receipts_frame = ttk.LabelFrame(main_frame, text="Receipts", padding="10", style='Dark.TLabelFrame')
        receipts_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        receipts_frame.columnconfigure(0, weight=1)
        
        # Receipts listbox with scrollbar
        receipts_list_frame = ttk.Frame(receipts_frame, style='Dark.TFrame')
        receipts_list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        receipts_list_frame.columnconfigure(0, weight=1)
        
        self.receipts_listbox = tk.Listbox(receipts_list_frame, height=4, 
                                         bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                         selectbackground=self.colors['terminal_green'], 
                                         selectforeground=self.colors['bg_primary'],
                                         font=('Monaco', 9))
        self.receipts_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        receipts_scrollbar = ttk.Scrollbar(receipts_list_frame, orient=tk.VERTICAL, 
                                          command=self.receipts_listbox.yview)
        receipts_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.receipts_listbox.configure(yscrollcommand=receipts_scrollbar.set)
        
        # Receipt input
        receipt_input_frame = ttk.Frame(receipts_frame, style='Dark.TFrame')
        receipt_input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        receipt_input_frame.columnconfigure(0, weight=1)
        
        self.receipt_entry = ttk.Entry(receipt_input_frame, width=15, style='Dark.TEntry')
        self.receipt_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.receipt_entry.bind('<Return>', lambda e: self.add_receipt())
        
        ttk.Button(receipt_input_frame, text="Add Receipt", 
                  command=self.add_receipt, style='Dark.TButton').grid(row=0, column=1, padx=(0, 5))
        ttk.Button(receipt_input_frame, text="Remove Selected", 
                  command=self.remove_receipt, style='Dark.TButton').grid(row=0, column=2)
        
        # Receipts total
        self.receipts_total_label = ttk.Label(receipts_frame, text="Total Receipts: £0.00", 
                                            font=('Monaco', 10, 'bold'), style='Dark.TLabel')
        self.receipts_total_label.grid(row=2, column=0, pady=(10, 0))
        
        # Additional Cash In section
        additional_cash_frame = ttk.LabelFrame(main_frame, text="Additional Cash In", padding="10", style='Dark.TLabelFrame')
        additional_cash_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        additional_cash_frame.columnconfigure(0, weight=1)
        
        # Additional cash listbox
        additional_cash_list_frame = ttk.Frame(additional_cash_frame, style='Dark.TFrame')
        additional_cash_list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        additional_cash_list_frame.columnconfigure(0, weight=1)
        
        self.additional_cash_listbox = tk.Listbox(additional_cash_list_frame, height=3, 
                                                bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                                selectbackground=self.colors['terminal_green'], 
                                                selectforeground=self.colors['bg_primary'],
                                                font=('Monaco', 9))
        self.additional_cash_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        additional_cash_scrollbar = ttk.Scrollbar(additional_cash_list_frame, orient=tk.VERTICAL, 
                                                 command=self.additional_cash_listbox.yview)
        additional_cash_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.additional_cash_listbox.configure(yscrollcommand=additional_cash_scrollbar.set)
        
        # Additional cash input
        additional_cash_input_frame = ttk.Frame(additional_cash_frame, style='Dark.TFrame')
        additional_cash_input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        additional_cash_input_frame.columnconfigure(0, weight=1)
        
        self.additional_cash_title_entry = ttk.Entry(additional_cash_input_frame, width=20, style='Dark.TEntry')
        self.additional_cash_title_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.additional_cash_title_entry.bind('<Return>', lambda e: self.add_additional_cash())
        
        self.additional_cash_amount_entry = ttk.Entry(additional_cash_input_frame, width=10, style='Dark.TEntry')
        self.additional_cash_amount_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 5))
        self.additional_cash_amount_entry.bind('<Return>', lambda e: self.add_additional_cash())
        
        ttk.Button(additional_cash_input_frame, text="Add", 
                  command=self.add_additional_cash, style='Dark.TButton').grid(row=0, column=2, padx=(0, 5))
        ttk.Button(additional_cash_input_frame, text="Remove Selected", 
                  command=self.remove_additional_cash, style='Dark.TButton').grid(row=0, column=3)
        
        # Additional cash total
        self.additional_cash_total_label = ttk.Label(additional_cash_frame, text="Total Additional Cash: £0.00", 
                                                    font=('Monaco', 10, 'bold'), style='Dark.TLabel')
        self.additional_cash_total_label.grid(row=2, column=0, pady=(10, 0))
        
        # Expected takings
        expected_frame = ttk.LabelFrame(main_frame, text="Expected Takings", padding="10", style='Dark.TLabelFrame')
        expected_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        expected_frame.columnconfigure(1, weight=1)
        
        ttk.Label(expected_frame, text="Expected Takings:", style='Dark.TLabel').grid(row=0, column=0, sticky=tk.W, pady=2)
        expected_entry = ttk.Entry(expected_frame, textvariable=self.expected_takings_var, width=15, style='Dark.TEntry')
        expected_entry.grid(row=0, column=1, sticky=tk.W, pady=2)
        expected_entry.bind('<KeyRelease>', lambda e: self.update_totals())
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10", style='Dark.TLabelFrame')
        results_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        results_frame.columnconfigure(0, weight=1)
        
        self.results_text = tk.Text(results_frame, height=8, width=70, wrap=tk.WORD,
                                  bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                  insertbackground=self.colors['terminal_green'],
                                  font=('Monaco', 9))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        results_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, 
                                         command=self.results_text.yview)
        results_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
        
        # Buttons
        button_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Calculate", 
                  command=self.calculate, style='Dark.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Save Report", 
                  command=self.save_report, style='Dark.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Clear All", 
                  command=self.clear_all, style='Dark.TButton').pack(side=tk.LEFT)
    
    def add_receipt(self):
        try:
            amount = float(self.receipt_entry.get())
            if amount < 0:
                messagebox.showerror("Error", "Please enter a positive amount.")
                return
            
            self.receipt_amounts.append(amount)
            self.receipts_listbox.insert(tk.END, f"Receipt #{len(self.receipt_amounts)}: £{amount:.2f}")
            self.receipt_entry.delete(0, tk.END)
            self.update_totals()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
    
    def remove_receipt(self):
        selection = self.receipts_listbox.curselection()
        if selection:
            index = selection[0]
            self.receipt_amounts.pop(index)
            self.receipts_listbox.delete(index)
            # Update display numbers
            self.receipts_listbox.delete(0, tk.END)
            for i, amount in enumerate(self.receipt_amounts):
                self.receipts_listbox.insert(tk.END, f"Receipt #{i+1}: £{amount:.2f}")
            self.update_totals()
    
    def add_additional_cash(self):
        try:
            title = self.additional_cash_title_entry.get().strip()
            amount = float(self.additional_cash_amount_entry.get())
            if not title:
                messagebox.showerror("Error", "Please enter a description.")
                return
            if amount < 0:
                messagebox.showerror("Error", "Please enter a positive amount.")
                return
            
            self.additional_cash_entries.append({'title': title, 'amount': amount})
            self.additional_cash_listbox.insert(tk.END, f"{title}: £{amount:.2f}")
            self.additional_cash_title_entry.delete(0, tk.END)
            self.additional_cash_amount_entry.delete(0, tk.END)
            self.update_totals()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
    
    def remove_additional_cash(self):
        selection = self.additional_cash_listbox.curselection()
        if selection:
            index = selection[0]
            self.additional_cash_entries.pop(index)
            self.additional_cash_listbox.delete(index)
            self.update_totals()
    
    def handle_cash_input_keys(self, event, input_index):
        """Handle key presses for cash input fields"""
        current_value = self.cash_counts[input_index].get()
        try:
            current_value = int(current_value) if current_value else 0
        except ValueError:
            current_value = 0
        
        new_value = current_value
        
        if event.keysym == 'space':
            new_value = current_value + 10
        elif event.keysym == 'Down':
            new_value = max(0, current_value - 10)
        elif event.keysym == 'Right':
            new_value = current_value + 1
        elif event.keysym == 'Left':
            new_value = max(0, current_value - 1)
        else:
            return  # Let other keys work normally
        
        self.cash_counts[input_index].set(new_value)
        self.update_totals()
    
    def update_totals(self):
        # Calculate cash total
        total_cash = self.calculator.calculate_denomination_total([var.get() for var in self.cash_counts])
        self.cash_total_label.config(text=f"Total Cash: £{total_cash:.2f}")
        
        # Calculate receipts total
        total_receipts = sum(self.receipt_amounts) if self.receipt_amounts else 0
        self.receipts_total_label.config(text=f"Total Receipts: £{total_receipts:.2f}")
        
        # Calculate additional cash total
        total_additional_cash = sum(entry['amount'] for entry in self.additional_cash_entries) if self.additional_cash_entries else 0
        self.additional_cash_total_label.config(text=f"Total Additional Cash: £{total_additional_cash:.2f}")
    
    def calculate(self):
        try:
            # Get values
            cash_counts = [var.get() for var in self.cash_counts]
            expected_takings = self.expected_takings_var.get()
            
            # Calculate analysis
            analysis = self.calculator.calculate_float_analysis(
                cash_counts, self.receipt_amounts, self.additional_cash_entries, expected_takings
            )
            bagging = self.calculator.generate_bagging_instructions(analysis, cash_counts)
            
            # Display results
            self.display_results(analysis, bagging)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error in calculation: {str(e)}")
    
    def display_results(self, analysis, bagging):
        self.results_text.delete(1.0, tk.END)
        
        result = f"CASH UP RESULTS - {self.date_var.get()}\n"
        result += "=" * 50 + "\n\n"
        
        # Summary
        result += "SUMMARY:\n"
        result += f"Total Cash: £{analysis['total_cash']:.2f}\n"
        result += f"Total Receipts: £{analysis['total_receipts']:.2f}\n"
        result += f"Total Additional Cash: £{analysis['total_additional_cash']:.2f} (already in till)\n"
        result += f"Total in Till: £{analysis['total_in_till']:.2f}\n"
        result += f"Expected Total: £{analysis['expected_total']:.2f}\n\n"
        
        # Float analysis
        result += "FLOAT ANALYSIS:\n"
        result += f"Starting Float: £{self.calculator.default_float:.2f}\n"
        result += f"Expected Takings: £{analysis['expected_takings']:.2f}\n"
        
        if analysis['is_exact']:
            result += "Result: EXACT BALANCE ✅\n\n"
        elif analysis['is_over']:
            result += f"Result: OVER by £{analysis['difference']:.2f} ✅\n\n"
        else:
            result += f"Result: SHORT by £{abs(analysis['difference']):.2f} ❌\n\n"
        
        # Bagging instructions
        result += "BAGGING INSTRUCTIONS:\n"
        if analysis['amount_to_remove'] > 0:
            result += f"Remove £{analysis['amount_to_remove']:.2f} total:\n"
            result += f"  - All receipts: £{analysis['total_receipts']:.2f}\n"
            result += f"  - Additional cash stays in till: £{analysis['total_additional_cash']:.2f}\n"
            
            if bagging['cash_to_remove'] > 0:
                result += f"  - Additional cash: £{bagging['cash_to_remove']:.2f}\n"
                if bagging['cash_suggestions']:
                    result += "  Suggested cash removal:\n"
                    for denom, count, value in bagging['cash_suggestions']:
                        result += f"    {count} × {denom} = £{value:.2f}\n"
            elif bagging['needs_additional_cash']:
                result += f"  - Add cash: £{bagging['additional_cash_needed']:.2f}\n"
        else:
            result += f"Add £{abs(analysis['amount_to_remove']):.2f} to reach £{self.calculator.default_float:.2f} float\n"
        
        result += f"Final till amount: £{self.calculator.default_float:.2f}\n"
        
        self.results_text.insert(1.0, result)
    
    def save_report(self):
        try:
            # Get values
            cash_counts = [var.get() for var in self.cash_counts]
            expected_takings = self.expected_takings_var.get()
            
            # Generate report content
            report_content = self.report_generator.generate_report_content(
                self.date_var.get(), cash_counts, self.receipt_amounts,
                self.additional_cash_entries, expected_takings, self.calculator
            )
            
            # Save to file
            success, result = self.report_generator.save_report_to_file(
                self.date_var.get(), report_content
            )
            
            if success:
                messagebox.showinfo("Success", f"Report saved successfully to:\n{result}")
            else:
                messagebox.showerror("Error", f"Error saving report:\n{result}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error saving report: {str(e)}")
    
    def clear_all(self):
        # Clear all inputs
        for var in self.cash_counts:
            var.set(0)
        
        self.receipt_amounts.clear()
        self.receipts_listbox.delete(0, tk.END)
        self.receipt_entry.delete(0, tk.END)
        
        self.additional_cash_entries.clear()
        self.additional_cash_listbox.delete(0, tk.END)
        self.additional_cash_title_entry.delete(0, tk.END)
        self.additional_cash_amount_entry.delete(0, tk.END)
        
        self.expected_takings_var.set(0)
        
        self.results_text.delete(1.0, tk.END)
        self.update_totals()

def main():
    root = tk.Tk()
    app = CashUpDesktopApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
