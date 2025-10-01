# CashUp - Cash Management Application

## 🌐 Live Application

**👉 [Click here to use the CashUp application](https://smissing.github.io/CashUp/)**

This is a comprehensive cash management application for businesses to track daily takings, calculate float differences, and generate detailed reports.

## Features

- **Real-time Calculations**: Instant totals and float analysis
- **Smart Bagging Instructions**: Suggests optimal cash removal
- **Report Generation**: Print and download daily reports
- **Modern UI**: Clean, intuitive interface design
- **No Installation Required**: Runs entirely in your browser

## Quick Start

1. Visit the [live application](https://smissing.github.io/CashUp/)
2. Enter today's date
3. Count and enter cash amounts for each denomination
4. Add receipt amounts and additional cash
5. Enter expected takings
6. Click "Calculate Cash Up" to see results
7. Print or download the report

## For Developers

This repository contains both the static web version (for GitHub Pages) and the full Python application with multiple interfaces.

### Local Development

```bash
# Clone the repository
git clone https://github.com/SMissing/CashUp.git
cd CashUp

# Install dependencies
pip install -r requirements.txt

# Run the launcher
python launcher.py
```

### File Structure

- `index.html` - Static web version (GitHub Pages)
- `main.py` - Command line interface
- `app.py` - Flask web application
- `desktop_app.py` - Desktop GUI application
- `launcher.py` - Application launcher

## License

This project is open source and available under the MIT License.
