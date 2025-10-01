"""
Configuration settings for the Cash Up Application
"""
import os

class Config:
    # Default float amount
    DEFAULT_FLOAT = 200.00
    
    # Currency settings
    CURRENCY_SYMBOL = "£"
    
    # Report settings
    REPORTS_DIR = "Reports"
    
    # Database settings (for future use)
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///cash_up.db'
    
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # UI settings - Terminal Dark Theme
    THEME_COLORS = {
        'bg_primary': '#0d1117',      # Dark background
        'bg_secondary': '#161b22',    # Secondary background
        'bg_tertiary': '#21262d',     # Tertiary background
        'text_primary': '#f0f6fc',    # Primary text
        'text_secondary': '#8b949e',  # Secondary text
        'text_muted': '#6e7681',      # Muted text
        'border_color': '#30363d',    # Border color
        'terminal_green': '#00ff00',  # Terminal green
        'terminal_amber': '#ffb000',  # Terminal amber
        'accent_green': '#3fb950',    # Accent green
        'accent_blue': '#58a6ff',     # Accent blue
        'accent_red': '#f85149',      # Accent red
        'accent_yellow': '#d29922',   # Accent yellow
        'accent_orange': '#ff7b72',   # Accent orange
        'accent_purple': '#a5a5ff'    # Accent purple
    }
