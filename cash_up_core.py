"""
Core business logic for the Cash Up Application
"""
from datetime import datetime
from typing import List, Tuple, Dict, Any
import os

class CashUpCalculator:
    """Handles all cash up calculations and business logic"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.denominations = ["1p", "2p", "5p", "10p", "20p", "50p", "£1", "£2", "£5", "£10", "£20", "£50"]
        self.values = [0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1.00, 2.00, 5.00, 10.00, 20.00, 50.00]
        self.default_float = self.config.get('DEFAULT_FLOAT', 200.00)
    
    def calculate_denomination_total(self, counts: List[int]) -> float:
        """Calculate total value for given counts and denomination values"""
        return sum(count * value for count, value in zip(counts, self.values))
    
    def suggest_change_removal(self, excess_amount: float, counts: List[int]) -> Tuple[List[Tuple[str, int, float]], float]:
        """Suggest which denominations to remove to get closest to target amount"""
        suggestions = []
        remaining = excess_amount
        
        # Work backwards from highest denomination
        for i in range(len(self.denominations)-1, -1, -1):
            if counts[i] > 0 and self.values[i] <= remaining:
                remove_count = min(counts[i], int(remaining / self.values[i]))
                if remove_count > 0:
                    suggestions.append((self.denominations[i], remove_count, remove_count * self.values[i]))
                    remaining -= remove_count * self.values[i]
        
        return suggestions, remaining
    
    def calculate_float_analysis(self, cash_counts: List[int], receipt_amounts: List[float], 
                                additional_cash_entries: List[Dict[str, Any]], expected_takings: float) -> Dict[str, Any]:
        """Calculate complete float analysis"""
        total_cash = self.calculate_denomination_total(cash_counts)
        total_receipts = sum(receipt_amounts) if receipt_amounts else 0
        total_additional_cash = sum(entry['amount'] for entry in additional_cash_entries) if additional_cash_entries else 0
        
        # Additional cash is already in the till, so we need to subtract it from the total
        # to get the actual takings that should be in the till
        total_in_till = total_cash + total_receipts
        expected_total = self.default_float + expected_takings
        difference = total_in_till - expected_total
        amount_to_remove = total_in_till - self.default_float
        
        return {
            'total_cash': total_cash,
            'total_receipts': total_receipts,
            'additional_cash_entries': additional_cash_entries,
            'total_additional_cash': total_additional_cash,
            'total_in_till': total_in_till,
            'expected_takings': expected_takings,
            'expected_total': expected_total,
            'difference': difference,
            'amount_to_remove': amount_to_remove,
            'is_over': difference > 0,
            'is_short': difference < 0,
            'is_exact': abs(difference) < 0.01
        }
    
    def generate_bagging_instructions(self, analysis: Dict[str, Any], cash_counts: List[int]) -> Dict[str, Any]:
        """Generate bagging instructions based on analysis"""
        instructions = {
            'total_to_remove': analysis['amount_to_remove'],
            'receipts_to_remove': analysis['total_receipts'],
            'additional_cash_entries': analysis['additional_cash_entries'],
            'total_additional_cash': analysis['total_additional_cash'],
            'cash_to_remove': 0,
            'cash_suggestions': [],
            'needs_additional_cash': False
        }
        
        if analysis['amount_to_remove'] > 0:
            # Only remove receipts and cash - additional cash stays in till
            cash_to_remove = analysis['amount_to_remove'] - analysis['total_receipts']
            instructions['cash_to_remove'] = cash_to_remove
            
            if cash_to_remove > 0:
                suggestions, remaining = self.suggest_change_removal(cash_to_remove, cash_counts)
                instructions['cash_suggestions'] = suggestions
                instructions['remaining_after_suggestions'] = remaining
            elif cash_to_remove < 0:
                instructions['needs_additional_cash'] = True
                instructions['additional_cash_needed'] = abs(cash_to_remove)
        
        return instructions

class ReportGenerator:
    """Handles report generation and file operations"""
    
    def __init__(self, reports_dir="Reports"):
        self.reports_dir = reports_dir
    
    def save_report_to_file(self, date_input: str, report_content: str) -> Tuple[bool, str]:
        """Save the cash up report to a text file with organized folder structure"""
        try:
            # Parse the date to create folder structure
            day, month, year = date_input.split('/')
            
            # Create the Reports folder structure
            year_dir = os.path.join(self.reports_dir, year)
            month_dir = os.path.join(year_dir, month.zfill(2))  # Ensure 2-digit month
            
            # Create directories if they don't exist
            os.makedirs(month_dir, exist_ok=True)
            
            # Create filename with full date
            filename = f"Cash_Up_{day.zfill(2)}-{month.zfill(2)}-{year}.txt"
            filepath = os.path.join(month_dir, filename)
            
            # Save the report
            with open(filepath, 'w') as f:
                f.write(report_content)
            
            return True, filepath
        except Exception as e:
            return False, str(e)
    
    def generate_report_content(self, date_input: str, cash_counts: List[int], 
                              receipt_amounts: List[float], additional_cash_entries: List[Dict[str, Any]],
                              expected_takings: float, calculator: CashUpCalculator) -> str:
        """Generate formatted report content"""
        analysis = calculator.calculate_float_analysis(cash_counts, receipt_amounts, 
                                                     additional_cash_entries, expected_takings)
        bagging = calculator.generate_bagging_instructions(analysis, cash_counts)
        
        report_lines = []
        report_lines.append("="*60)
        report_lines.append(f"CASH UP - {date_input}")
        report_lines.append("="*60)
        
        # Cash breakdown
        report_lines.append("\nCASH BREAKDOWN:")
        for i, (denom, count, value) in enumerate(zip(calculator.denominations, cash_counts, calculator.values)):
            if count > 0:
                total_value = count * value
                line = f"  {denom}: {count} × £{value:.2f} = £{total_value:.2f}"
                report_lines.append(line)
        report_lines.append(f"  Total Cash: £{analysis['total_cash']:.2f}")
        
        # Receipt breakdown
        if receipt_amounts:
            report_lines.append("\nRECEIPT BREAKDOWN:")
            for i, amount in enumerate(receipt_amounts):
                line = f"  Receipt #{i+1}: £{amount:.2f}"
                report_lines.append(line)
            report_lines.append(f"  Total Receipts: £{analysis['total_receipts']:.2f}")
        else:
            report_lines.append("\nRECEIPTS: None")
        
        # Additional cash breakdown
        if additional_cash_entries:
            report_lines.append("\nADDITIONAL CASH IN:")
            for i, entry in enumerate(additional_cash_entries):
                report_lines.append(f"  {entry['title']}: £{entry['amount']:.2f}")
            report_lines.append(f"  Total Additional Cash: £{analysis['total_additional_cash']:.2f}")
        else:
            report_lines.append("\nADDITIONAL CASH IN: None")
        
        # Summary
        report_lines.append("\nSUMMARY:")
        report_lines.append(f"  Starting Float: £{calculator.default_float:.2f}")
        report_lines.append(f"  Expected Takings: £{expected_takings:.2f}")
        report_lines.append(f"  Expected Total: £{analysis['expected_total']:.2f}")
        report_lines.append(f"  Actual Total: £{analysis['total_in_till']:.2f}")
        report_lines.append(f"    (Cash: £{analysis['total_cash']:.2f} + Receipts: £{analysis['total_receipts']:.2f})")
        report_lines.append(f"  Additional Cash In: £{analysis['total_additional_cash']:.2f} (already in till)")
        
        if analysis['is_exact']:
            report_lines.append("  Result: EXACT BALANCE")
        elif analysis['is_over']:
            report_lines.append(f"  Result: OVER by £{analysis['difference']:.2f}")
        else:
            report_lines.append(f"  Result: SHORT by £{abs(analysis['difference']):.2f}")
        
        # Bagging instructions
        report_lines.append("\nBAGGING INSTRUCTIONS:")
        if analysis['amount_to_remove'] > 0:
            report_lines.append(f"  Remove £{analysis['amount_to_remove']:.2f} total:")
            report_lines.append(f"    - All receipts: £{analysis['total_receipts']:.2f}")
            report_lines.append(f"    - Additional cash stays in till: £{analysis['total_additional_cash']:.2f}")
            
            if bagging['cash_to_remove'] > 0:
                report_lines.append(f"    - Additional cash: £{bagging['cash_to_remove']:.2f}")
            elif bagging['needs_additional_cash']:
                report_lines.append(f"    - Add cash: £{bagging['additional_cash_needed']:.2f}")
        else:
            report_lines.append(f"  Add £{abs(analysis['amount_to_remove']):.2f} to reach £{calculator.default_float:.2f} float")
        
        report_lines.append(f"  Final till amount: £{calculator.default_float:.2f}")
        report_lines.append("\n" + "="*60)
        report_lines.append("CASH UP COMPLETE")
        report_lines.append("="*60)
        
        return "\n".join(report_lines)
