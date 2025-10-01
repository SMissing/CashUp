#!/usr/bin/env python3
"""
Cash Up Application
Handles counting coins, notes, receipts and calculates float differences
"""

import os

def get_coin_count(denomination):
    """Get the count of a specific coin/note denomination"""
    while True:
        try:
            count = int(input(f"How many {denomination} do you have? "))
            if count < 0:
                print("Please enter a positive number.")
                continue
            return count
        except ValueError:
            print("Please enter a valid number.")

def get_receipt_amounts(receipt_count):
    """Get the amounts for each receipt"""
    receipt_amounts = []
    for i in range(receipt_count):
        while True:
            try:
                amount = float(input(f"How much was receipt #{i+1}? £"))
                if amount < 0:
                    print("Please enter a positive amount.")
                    continue
                receipt_amounts.append(amount)
                break
            except ValueError:
                print("Please enter a valid amount.")
    return receipt_amounts

def calculate_denomination_total(counts, values):
    """Calculate total value for given counts and denomination values"""
    return sum(count * value for count, value in zip(counts, values))

def suggest_change_removal(excess_amount, counts, values, denominations):
    """Suggest which denominations to remove to get closest to target amount"""
    suggestions = []
    remaining = excess_amount
    
    # Work backwards from highest denomination
    for i in range(len(denominations)-1, -1, -1):
        if counts[i] > 0 and values[i] <= remaining:
            remove_count = min(counts[i], int(remaining / values[i]))
            if remove_count > 0:
                suggestions.append((denominations[i], remove_count, remove_count * values[i]))
                remaining -= remove_count * values[i]
    
    return suggestions, remaining

def review_and_modify_counts(denominations, counts, values):
    """Allow user to review and modify denomination counts"""
    while True:
        print("\n--- CURRENT CASH COUNTS ---")
        for i, (denom, count, value) in enumerate(zip(denominations, counts, values)):
            if count > 0:
                total_value = count * value
                print(f"{i+1}. {denom}: {count} × £{value:.2f} = £{total_value:.2f}")
        
        total_cash = calculate_denomination_total(counts, values)
        print(f"\nTotal cash: £{total_cash:.2f}")
        
        choice = input("\nEnter number to modify (or 'done' to continue): ").strip().lower()
        
        if choice == 'done':
            break
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(denominations):
                new_count = get_coin_count(denominations[index])
                counts[index] = new_count
                print(f"Updated {denominations[index]} count to {new_count}")
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Please enter a valid number or 'done'.")
    
    return counts

def review_and_modify_receipts(receipt_amounts):
    """Allow user to review and modify receipt amounts"""
    while True:
        print("\n--- CURRENT RECEIPTS ---")
        if not receipt_amounts:
            print("No receipts entered.")
        else:
            for i, amount in enumerate(receipt_amounts):
                print(f"{i+1}. Receipt #{i+1}: £{amount:.2f}")
        
        total_receipts = sum(receipt_amounts) if receipt_amounts else 0
        print(f"\nTotal receipts: £{total_receipts:.2f}")
        
        print("\nOptions:")
        print("1. Modify existing receipt")
        print("2. Add new receipt")
        print("3. Remove receipt")
        print("4. Done")
        
        choice = input("Choose option (1-4): ").strip()
        
        if choice == '4':
            break
        elif choice == '1' and receipt_amounts:
            try:
                index = int(input(f"Which receipt to modify (1-{len(receipt_amounts)})? ")) - 1
                if 0 <= index < len(receipt_amounts):
                    while True:
                        try:
                            new_amount = float(input(f"New amount for receipt #{index+1}: £"))
                            if new_amount < 0:
                                print("Please enter a positive amount.")
                                continue
                            receipt_amounts[index] = new_amount
                            print(f"Updated receipt #{index+1} to £{new_amount:.2f}")
                            break
                        except ValueError:
                            print("Please enter a valid amount.")
                else:
                    print("Invalid receipt number.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '2':
            while True:
                try:
                    new_amount = float(input(f"Amount for new receipt: £"))
                    if new_amount < 0:
                        print("Please enter a positive amount.")
                        continue
                    receipt_amounts.append(new_amount)
                    print(f"Added new receipt: £{new_amount:.2f}")
                    break
                except ValueError:
                    print("Please enter a valid amount.")
        elif choice == '3' and receipt_amounts:
            try:
                index = int(input(f"Which receipt to remove (1-{len(receipt_amounts)})? ")) - 1
                if 0 <= index < len(receipt_amounts):
                    removed_amount = receipt_amounts.pop(index)
                    print(f"Removed receipt: £{removed_amount:.2f}")
                else:
                    print("Invalid receipt number.")
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("Invalid choice or no receipts to modify.")
    
    return receipt_amounts

def save_report_to_file(date_input, report_content):
    """Save the cash up report to a text file with organized folder structure"""
    # Parse the date to create folder structure
    day, month, year = date_input.split('/')
    
    # Create the Reports folder structure
    reports_dir = "Reports"
    year_dir = os.path.join(reports_dir, year)
    month_dir = os.path.join(year_dir, month.zfill(2))  # Ensure 2-digit month
    
    # Create directories if they don't exist
    os.makedirs(month_dir, exist_ok=True)
    
    # Create filename with full date
    filename = f"Cash_Up_{day.zfill(2)}-{month.zfill(2)}-{year}.txt"
    filepath = os.path.join(month_dir, filename)
    
    # Check if file already exists
    if os.path.exists(filepath):
        while True:
            overwrite = input(f"\nA cash up report for {date_input} already exists.\nDo you want to overwrite it? (y/n): ").strip().lower()
            if overwrite in ['y', 'yes']:
                break
            elif overwrite in ['n', 'no']:
                print("Report not saved.")
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
    
    # Save the report
    try:
        with open(filepath, 'w') as f:
            f.write(report_content)
        print(f"\nReport saved successfully to: {filepath}")
        return True
    except Exception as e:
        print(f"\nError saving report: {e}")
        return False

def main():
    print("=== CASH UP APPLICATION ===\n")
    
    # Get today's date
    print("--- DATE ENTRY ---")
    while True:
        date_input = input("Enter today's date (DD/MM/YYYY): ").strip()
        if len(date_input) == 10 and date_input[2] == '/' and date_input[5] == '/':
            try:
                day, month, year = date_input.split('/')
                day, month, year = int(day), int(month), int(year)
                if 1 <= day <= 31 and 1 <= month <= 12 and 2000 <= year <= 2100:
                    print(f"Cash up for: {date_input}")
                    break
                else:
                    print("Please enter a valid date (DD/MM/YYYY).")
            except ValueError:
                print("Please enter a valid date format (DD/MM/YYYY).")
        else:
            print("Please enter date in DD/MM/YYYY format.")
    
    print()  # Add spacing
    
    # Define denominations and their values
    denominations = ["1p", "2p", "5p", "10p", "20p", "50p", "£1", "£2", "£5", "£10", "£20", "£50"]
    values = [0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1.00, 2.00, 5.00, 10.00, 20.00, 50.00]
    
    # Get counts for each denomination
    print("Count your cash:")
    counts = []
    for denom in denominations:
        count = get_coin_count(denom)
        counts.append(count)
    
    # Get receipt information
    print("\n--- RECEIPTS ---")
    while True:
        try:
            receipt_count = int(input("How many receipts do you have? "))
            if receipt_count < 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    receipt_amounts = []
    if receipt_count > 0:
        receipt_amounts = get_receipt_amounts(receipt_count)
    
    # Get air hockey machine earnings
    print("\n--- AIR HOCKEY MACHINE ---")
    while True:
        try:
            air_hockey_earnings = float(input("How much was made from the air hockey machine? £"))
            if air_hockey_earnings < 0:
                print("Please enter a positive amount.")
                continue
            break
        except ValueError:
            print("Please enter a valid amount.")
    
    # Get expected takings
    print("\n--- EXPECTED TAKINGS ---")
    while True:
        try:
            expected_takings = float(input("How much should have been made today? £"))
            if expected_takings < 0:
                print("Please enter a positive amount.")
                continue
            break
        except ValueError:
            print("Please enter a valid amount.")
    
    # Main calculation and review loop
    while True:
        # Calculate totals
        total_cash = calculate_denomination_total(counts, values)
        total_receipts = sum(receipt_amounts) if receipt_amounts else 0
        total_with_air_hockey = total_cash + total_receipts + air_hockey_earnings
        
        # Display current totals
        print(f"\n--- CASH BREAKDOWN ---")
        for i, (denom, count, value) in enumerate(zip(denominations, counts, values)):
            if count > 0:
                total_value = count * value
                print(f"{denom}: {count} × £{value:.2f} = £{total_value:.2f}")
        print(f"\nTotal cash in till: £{total_cash:.2f}")
        
        if receipt_amounts:
            print(f"\n--- RECEIPT BREAKDOWN ---")
            for i, amount in enumerate(receipt_amounts):
                print(f"Receipt #{i+1}: £{amount:.2f}")
            print(f"Total receipts: £{total_receipts:.2f}")
        else:
            print("\nNo receipts to process.")
        
        print(f"\n--- AIR HOCKEY MACHINE ---")
        print(f"Air hockey earnings: £{air_hockey_earnings:.2f}")
        
        # Calculate float analysis
        print("\n=== FLOAT ANALYSIS ===")
        float_amount = 200.00
        total_in_till = total_with_air_hockey
        expected_total = float_amount + expected_takings
        difference = total_in_till - expected_total
        
        print(f"Starting float: £{float_amount:.2f}")
        print(f"Expected takings: £{expected_takings:.2f}")
        print(f"Expected total in till: £{expected_total:.2f}")
        print(f"Actual total in till: £{total_in_till:.2f}")
        print(f"  (Cash: £{total_cash:.2f} + Receipts: £{total_receipts:.2f} + Air Hockey: £{air_hockey_earnings:.2f})")
        
        if difference > 0:
            print(f"✅ OVER by: £{difference:.2f}")
        elif difference < 0:
            print(f"❌ SHORT by: £{abs(difference):.2f}")
        else:
            print("✅ EXACT - Perfect balance!")
        
        # Calculate what to bag up
        print(f"\n=== BAGGING INSTRUCTIONS ===")
        amount_to_remove = total_in_till - float_amount
        
        if amount_to_remove > 0:
            print(f"Remove £{amount_to_remove:.2f} to restore £{float_amount:.2f} float")
            print(f"This includes:")
            print(f"  - All receipts: £{total_receipts:.2f}")
            print(f"  - Air hockey earnings: £{air_hockey_earnings:.2f}")
            
            cash_to_remove = amount_to_remove - total_receipts - air_hockey_earnings
            if cash_to_remove > 0:
                print(f"  - Additional cash: £{cash_to_remove:.2f}")
                
                # Suggest best denominations to remove
                print(f"\n--- SUGGESTED CASH REMOVAL ---")
                suggestions, remaining = suggest_change_removal(cash_to_remove, counts, values, denominations)
                
                if suggestions:
                    total_suggested = 0
                    for denom, count, value in suggestions:
                        print(f"Remove {count} × {denom} = £{value:.2f}")
                        total_suggested += value
                    
                    if remaining > 0.01:  # Account for rounding
                        print(f"Remaining to remove: £{remaining:.2f}")
                        print("(You may need to make change with smaller denominations)")
                else:
                    print("Not enough large denominations available for optimal removal.")
            elif cash_to_remove < 0:
                print(f"  - Need to add cash: £{abs(cash_to_remove):.2f}")
        else:
            print(f"Add £{abs(amount_to_remove):.2f} to reach £{float_amount:.2f} float")
        
        print(f"\nAfter bagging, till should contain exactly £{float_amount:.2f}")
        
        # Ask if user wants to modify anything
        print("\n=== REVIEW AND MODIFY ===")
        print("1. Modify cash counts")
        print("2. Modify receipts")
        print("3. Modify air hockey earnings")
        print("4. Change expected takings")
        print("5. Finish (all correct)")
        
        choice = input("\nChoose option (1-5): ").strip()
        
        if choice == '1':
            counts = review_and_modify_counts(denominations, counts, values)
        elif choice == '2':
            receipt_amounts = review_and_modify_receipts(receipt_amounts)
        elif choice == '3':
            while True:
                try:
                    air_hockey_earnings = float(input("New air hockey earnings amount: £"))
                    if air_hockey_earnings < 0:
                        print("Please enter a positive amount.")
                        continue
                    print(f"Updated air hockey earnings to £{air_hockey_earnings:.2f}")
                    break
                except ValueError:
                    print("Please enter a valid amount.")
        elif choice == '4':
            while True:
                try:
                    expected_takings = float(input("New expected takings amount: £"))
                    if expected_takings < 0:
                        print("Please enter a positive amount.")
                        continue
                    print(f"Updated expected takings to £{expected_takings:.2f}")
                    break
                except ValueError:
                    print("Please enter a valid amount.")
        elif choice == '5':
            # Generate final report
            print("\n" + "="*60)
            print(f"CASH UP - {date_input}")
            print("="*60)
            
            # Final calculations
            final_total_cash = calculate_denomination_total(counts, values)
            final_total_receipts = sum(receipt_amounts) if receipt_amounts else 0
            final_total_in_till = final_total_cash + final_total_receipts + air_hockey_earnings
            final_expected_total = float_amount + expected_takings
            final_difference = final_total_in_till - final_expected_total
            final_amount_to_remove = final_total_in_till - float_amount
            
            # Build report content for both display and file saving
            report_lines = []
            report_lines.append("="*60)
            report_lines.append(f"CASH UP - {date_input}")
            report_lines.append("="*60)
            
            # Cash breakdown
            report_lines.append("\nCASH BREAKDOWN:")
            for i, (denom, count, value) in enumerate(zip(denominations, counts, values)):
                if count > 0:
                    total_value = count * value
                    line = f"  {denom}: {count} × £{value:.2f} = £{total_value:.2f}"
                    report_lines.append(line)
                    print(line)
            cash_total_line = f"  Total Cash: £{final_total_cash:.2f}"
            report_lines.append(cash_total_line)
            print(cash_total_line)
            
            # Receipt breakdown
            if receipt_amounts:
                receipt_header = "\nRECEIPT BREAKDOWN:"
                report_lines.append(receipt_header)
                print(receipt_header)
                for i, amount in enumerate(receipt_amounts):
                    line = f"  Receipt #{i+1}: £{amount:.2f}"
                    report_lines.append(line)
                    print(line)
                receipt_total_line = f"  Total Receipts: £{final_total_receipts:.2f}"
                report_lines.append(receipt_total_line)
                print(receipt_total_line)
            else:
                no_receipts_line = "\nRECEIPTS: None"
                report_lines.append(no_receipts_line)
                print(no_receipts_line)
            
            # Air hockey breakdown
            air_hockey_header = "\nAIR HOCKEY MACHINE:"
            air_hockey_line = f"  Air hockey earnings: £{air_hockey_earnings:.2f}"
            report_lines.append(air_hockey_header)
            report_lines.append(air_hockey_line)
            print(air_hockey_header)
            print(air_hockey_line)
            
            # Summary
            summary_header = "\nSUMMARY:"
            report_lines.append(summary_header)
            print(summary_header)
            
            summary_lines = [
                f"  Starting Float: £{float_amount:.2f}",
                f"  Expected Takings: £{expected_takings:.2f}",
                f"  Expected Total: £{final_expected_total:.2f}",
                f"  Actual Total: £{final_total_in_till:.2f}",
                f"    (Cash: £{final_total_cash:.2f} + Receipts: £{final_total_receipts:.2f} + Air Hockey: £{air_hockey_earnings:.2f})"
            ]
            
            for line in summary_lines:
                report_lines.append(line)
                print(line)
            
            if final_difference > 0:
                result_line = f"  Result: OVER by £{final_difference:.2f}"
            elif final_difference < 0:
                result_line = f"  Result: SHORT by £{abs(final_difference):.2f}"
            else:
                result_line = f"  Result: EXACT BALANCE"
            
            report_lines.append(result_line)
            print(result_line + (" ✅" if final_difference >= 0 else " ❌"))
            
            # Bagging instructions
            bagging_header = "\nBAGGING INSTRUCTIONS:"
            report_lines.append(bagging_header)
            print(bagging_header)
            
            if final_amount_to_remove > 0:
                remove_line = f"  Remove £{final_amount_to_remove:.2f} total:"
                receipts_line = f"    - All receipts: £{final_total_receipts:.2f}"
                air_hockey_line = f"    - Air hockey earnings: £{air_hockey_earnings:.2f}"
                report_lines.extend([remove_line, receipts_line, air_hockey_line])
                print(remove_line)
                print(receipts_line)
                print(air_hockey_line)
                
                cash_to_remove = final_amount_to_remove - final_total_receipts - air_hockey_earnings
                if cash_to_remove > 0:
                    cash_line = f"    - Additional cash: £{cash_to_remove:.2f}"
                    report_lines.append(cash_line)
                    print(cash_line)
                elif cash_to_remove < 0:
                    add_cash_line = f"    - Add cash: £{abs(cash_to_remove):.2f}"
                    report_lines.append(add_cash_line)
                    print(add_cash_line)
            else:
                add_line = f"  Add £{abs(final_amount_to_remove):.2f} to reach £{float_amount:.2f} float"
                report_lines.append(add_line)
                print(add_line)
            
            final_till_line = f"  Final till amount: £{float_amount:.2f}"
            report_lines.append(final_till_line)
            print(final_till_line)
            
            report_lines.append("\n" + "="*60)
            report_lines.append("CASH UP COMPLETE")
            report_lines.append("="*60)
            
            print("\n" + "="*60)
            print("CASH UP COMPLETE")
            print("="*60)
            
            # Save report to file
            report_content = "\n".join(report_lines)
            save_report_to_file(date_input, report_content)
            
            break
        else:
            print("Invalid choice. Please try again.")
        
        print("\n" + "="*50)  # Separator line for clarity

if __name__ == "__main__":
    main()