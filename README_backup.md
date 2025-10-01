# Cash Up Application

A comprehensive cash management application for businesses to track daily takings, calculate float differences, and generate detailed reports.

## 🌐 Live Demo

**Try the application now**: [https://smissing.github.io/CashUp/](https://smissing.github.io/CashUp/)

The application runs entirely in your browser - no installation required!

## Features

- **Multiple Interfaces**: Web, Desktop GUI, and Command Line
- **Real-time Calculations**: Instant totals and float analysis
- **Smart Bagging Instructions**: Suggests optimal cash removal
- **Report Generation**: Automatic saving of daily reports
- **Historical Data**: Organized folder structure for reports
- **Modern UI**: Clean, intuitive interface design

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Quick Setup

1. **Clone or download** this repository to your local machine

2. **Navigate** to the cash_up directory:
   ```bash
   cd cash_up
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the launcher**:
   ```bash
   python launcher.py
   ```

## Usage

### Launcher Menu

The launcher provides three interface options:

1. **Web Interface** - Modern browser-based interface
   - Access at `http://localhost:5001`
   - Works on any device with a web browser
   - Real-time calculations and modern UI

2. **Desktop GUI** - Native desktop application
   - Traditional desktop interface
   - Works completely offline
   - Built with tkinter

3. **Command Line** - Terminal-based interface
   - Original interface design
   - Fast and lightweight
   - Perfect for quick calculations

### Web Interface

**Option 1: Live Demo (Recommended)**
1. Visit [https://smissing.github.io/CashUp/](https://smissing.github.io/CashUp/)
2. No installation required - works in any modern browser

**Option 2: Local Development**
1. Open your browser and go to `http://localhost:5001`
2. Enter today's date
3. Count and enter cash amounts for each denomination
4. Add receipt amounts
5. Enter additional cash (air hockey, vending, etc.)
6. Enter expected takings
7. Click "Calculate Cash Up" to see results
8. Print or download the report

### Desktop GUI

1. Run `python desktop_app.py` or use the launcher
2. Fill in all the required fields
3. Click "Calculate" to see results
4. Use "Save Report" to save to file
5. Use "Clear All" to start over

### Command Line

1. Run `python main.py` or use the launcher
2. Follow the interactive prompts
3. Review and modify entries as needed
4. Reports are automatically saved

## Configuration

Edit `config.py` to customize:

- Default float amount
- Currency symbol
- Report directory location
- UI theme colors

## File Structure

```
cash_up/
├── main.py              # Original command line interface
├── app.py               # Flask web application
├── desktop_app.py       # Tkinter desktop GUI
├── launcher.py          # Application launcher
├── cash_up_core.py      # Core business logic
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── templates/           # Web interface templates
│   ├── base.html
│   ├── index.html
│   └── results.html
└── Reports/             # Generated reports
    └── YYYY/
        └── MM/
            └── Cash_Up_DD-MM-YYYY.txt
```

## Report Format

Reports are automatically saved in the `Reports/` directory with the following structure:
- `Reports/YYYY/MM/Cash_Up_DD-MM-YYYY.txt`

Each report includes:
- Complete cash breakdown by denomination
- Receipt details
- Air hockey machine earnings
- Float analysis (over/short/exact)
- Detailed bagging instructions
- Summary totals

## Troubleshooting

### Common Issues

1. **Port already in use (Web Interface)**
   - The web interface uses port 5000 by default
   - Stop other applications using port 5000 or modify `app.py`

2. **Missing dependencies**
   - Run `pip install -r requirements.txt`
   - Ensure you're using Python 3.7+

3. **Permission errors (Report saving)**
   - Ensure the application has write permissions in the directory
   - Check that the `Reports/` folder exists

4. **Tkinter not available (Desktop GUI)**
   - On Linux: `sudo apt-get install python3-tk`
   - On macOS: Usually included with Python
   - On Windows: Usually included with Python

### Getting Help

If you encounter issues:
1. Check the error messages in the terminal
2. Ensure all dependencies are installed
3. Verify Python version compatibility
4. Check file permissions

## Development

### Adding New Features

1. Core business logic: `cash_up_core.py`
2. Web interface: `app.py` and `templates/`
3. Desktop GUI: `desktop_app.py`
4. Configuration: `config.py`

### Testing

Run each interface separately:
- Web: `python app.py`
- Desktop: `python desktop_app.py`
- CLI: `python main.py`

## License

This project is open source and available under the MIT License.

## Support

For support or feature requests, please create an issue in the project repository.
