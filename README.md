# Shortcut Popup App

A Python-based application that shows a clipboard manager popup when you double-press a specific key (default: 'S').

## Features
- **Global Hotkey**: Double-press 'S' to open.
- **Clipboard Integration**: Click an item to copy it to the clipboard.
- **Modern UI**: Dark themed, frameless popup.
- **Auto-close**: Closes on click or when you click away (focus loss).

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python main.py
   ```

## Configuration
You can modify `main.py` to change:
- `TRIGGER_KEY`: The key to listen for.
- `TEXT_ITEMS`: The list of text snippets to display.
- `DOUBLE_PRESS_THRESHOLD`: The speed required for the double press.
