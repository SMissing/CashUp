"""
Flask web application for Cash Up
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import os
from cash_up_core import CashUpCalculator, ReportGenerator
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize core components
calculator = CashUpCalculator({
    'DEFAULT_FLOAT': Config.DEFAULT_FLOAT
})
report_generator = ReportGenerator(Config.REPORTS_DIR)

@app.route('/')
def index():
    """Main cash up page"""
    today_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', 
                         denominations=calculator.denominations,
                         values=calculator.values,
                         default_float=calculator.default_float,
                         today_date=today_date)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate cash up results"""
    try:
        # Get form data
        date_input = request.form.get('date')
        
        # Convert date from YYYY-MM-DD to DD/MM/YYYY if needed
        if '-' in date_input:
            try:
                date_obj = datetime.strptime(date_input, '%Y-%m-%d')
                date_input = date_obj.strftime('%d/%m/%Y')
            except ValueError:
                pass  # Keep original format if conversion fails
        
        cash_counts = [int(request.form.get(f'count_{i}', 0)) for i in range(len(calculator.denominations))]
        receipt_amounts = [float(amount) for amount in request.form.getlist('receipt_amounts') if amount.strip()]
        expected_takings = float(request.form.get('expected_takings', 0))
        
        # Parse additional cash entries
        additional_cash_entries = []
        additional_titles = request.form.getlist('additional_cash_titles')
        additional_amounts = request.form.getlist('additional_cash_amounts')
        
        for title, amount in zip(additional_titles, additional_amounts):
            if title.strip() and amount.strip():
                try:
                    additional_cash_entries.append({
                        'title': title.strip(),
                        'amount': float(amount)
                    })
                except ValueError:
                    pass  # Skip invalid entries
        
        # Calculate analysis
        analysis = calculator.calculate_float_analysis(cash_counts, receipt_amounts, 
                                                     additional_cash_entries, expected_takings)
        bagging = calculator.generate_bagging_instructions(analysis, cash_counts)
        
        return render_template('results.html',
                             date=date_input,
                             denominations=calculator.denominations,
                             values=calculator.values,
                             cash_counts=cash_counts,
                             receipt_amounts=receipt_amounts,
                             additional_cash_entries=additional_cash_entries,
                             expected_takings=expected_takings,
                             analysis=analysis,
                             bagging=bagging)
    
    except Exception as e:
        flash(f'Error in calculation: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/save_report', methods=['POST'])
def save_report():
    """Save report to file"""
    try:
        date_input = request.form.get('date')
        
        # Convert date from YYYY-MM-DD to DD/MM/YYYY if needed
        if '-' in date_input:
            try:
                from datetime import datetime
                date_obj = datetime.strptime(date_input, '%Y-%m-%d')
                date_input = date_obj.strftime('%d/%m/%Y')
            except ValueError:
                pass  # Keep original format if conversion fails
        
        cash_counts = [int(request.form.get(f'count_{i}', 0)) for i in range(len(calculator.denominations))]
        receipt_amounts = [float(amount) for amount in request.form.getlist('receipt_amounts') if amount.strip()]
        expected_takings = float(request.form.get('expected_takings', 0))
        
        # Parse additional cash entries
        additional_cash_entries = []
        additional_titles = request.form.getlist('additional_cash_titles')
        additional_amounts = request.form.getlist('additional_cash_amounts')
        
        for title, amount in zip(additional_titles, additional_amounts):
            if title.strip() and amount.strip():
                try:
                    additional_cash_entries.append({
                        'title': title.strip(),
                        'amount': float(amount)
                    })
                except ValueError:
                    pass  # Skip invalid entries
        
        # Generate report content
        report_content = report_generator.generate_report_content(
            date_input, cash_counts, receipt_amounts, 
            additional_cash_entries, expected_takings, calculator
        )
        
        # Save to file
        success, result = report_generator.save_report_to_file(date_input, report_content)
        
        if success:
            flash(f'Report saved successfully to: {result}', 'success')
        else:
            flash(f'Error saving report: {result}', 'error')
        
        return redirect(url_for('index'))
    
    except Exception as e:
        print(f"Save report error: {str(e)}")  # Debug logging
        import traceback
        traceback.print_exc()  # Print full traceback for debugging
        flash(f'Error saving report: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """API endpoint for calculations"""
    try:
        data = request.get_json()
        cash_counts = data.get('cash_counts', [])
        receipt_amounts = data.get('receipt_amounts', [])
        air_hockey_earnings = data.get('air_hockey_earnings', 0)
        expected_takings = data.get('expected_takings', 0)
        
        analysis = calculator.calculate_float_analysis(cash_counts, receipt_amounts, 
                                                     air_hockey_earnings, expected_takings)
        bagging = calculator.generate_bagging_instructions(analysis, cash_counts)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'bagging': bagging
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
