import tkinter as tk
from tkinter import ttk
import keyboard
import pyperclip
import time
import sys
import threading

# Configuration
TRIGGER_KEY = 'x'
DOUBLE_PRESS_THRESHOLD = 0.25  # seconds (fast double tap)
def load_snippets():
    try:
        with open("snippets.txt", "r", encoding="utf-8") as f:
            return [line.strip().replace('\\n', '\n') for line in f if line.strip()]
    except FileNotFoundError:
        return ["Error: snippets.txt not found"]

TEXT_ITEMS = load_snippets()

class ModernPopup(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()  # Start hidden
        
        # Window setup
        self.overrideredirect(True)  # Remove window decorations
        self.attributes('-topmost', True)  # Keep on top
        self.configure(bg='#1e1e1e')
        
        # Dimensions and positioning (will be set on show)
        self.width = 300
        self.height = 0 # Auto-calculated
        
        # Styles
        self.title_font = ("Segoe UI", 10, "bold")
        self.item_font = ("Segoe UI", 10)
        self.bg_color = "#1e1e1e"
        self.hover_color = "#3a3a3a"
        self.text_color = "#ffffff"
        
        # Main container
        self.container = tk.Frame(self, bg=self.bg_color, highlightthickness=1, highlightbackground="#444444")
        self.container.pack(fill='both', expand=True)
        
        # Title (Optional)
        # lbl = tk.Label(self.container, text="Quick Copy", bg=self.bg_color, fg="#888888", font=("Segoe UI", 8), anchor='w', padx=10, pady=5)
        # lbl.pack(fill='x')

        # Create list items
        self.create_items()
        
        # Bindings
        self.bind("<Escape>", lambda e: self.hide_window())
        self.bind("<FocusOut>", lambda e: self.hide_window())

    def create_items(self):
        for text in TEXT_ITEMS:
            # Container for the item to handle hover properly
            item_frame = tk.Frame(self.container, bg=self.bg_color)
            item_frame.pack(fill='x', padx=1, pady=1)
            
            # Label for text (simulating button for better styling control)
            lbl = tk.Label(item_frame, 
                           text=text, 
                           bg=self.bg_color, 
                           fg=self.text_color, 
                           font=self.item_font, 
                           anchor="w", 
                           padx=10, 
                           pady=8,
                           cursor="hand2")
            lbl.pack(fill='x')
            
            # Events
            lbl.bind("<Button-1>", lambda e, t=text: self.on_item_click(t))
            lbl.bind("<Enter>", lambda e, f=item_frame, l=lbl: self.on_hover(f, l, True))
            lbl.bind("<Leave>", lambda e, f=item_frame, l=lbl: self.on_hover(f, l, False))

    def on_hover(self, frame, label, is_hovering):
        color = self.hover_color if is_hovering else self.bg_color
        frame.configure(bg=color)
        label.configure(bg=color)

    def on_item_click(self, text):
        pyperclip.copy(text)
        self.hide_window()
        # Optional: Show a small tooltip or visual feedback? 
        # For now, just close.

    def show_window(self):
        # Get mouse position
        x = self.winfo_pointerx()
        y = self.winfo_pointery()
        
        # Adjust position to not go off screen (basic logic)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate height based on items (approx)
        estimated_height = len(TEXT_ITEMS) * 40 + 20
        
        if x + self.width > screen_width:
            x = screen_width - self.width - 10
        if y + estimated_height > screen_height:
            y = screen_height - estimated_height - 10
            
        self.geometry(f"{self.width}x{estimated_height}+{x}+{y}")
        self.deiconify()
        self.lift()
        self.focus_force()

    def hide_window(self):
        self.withdraw()

def run_app():
    app = ModernPopup()
    
    # Global state for key detection
    last_s_press = 0
    
    def on_key(e):
        nonlocal last_s_press
        if e.event_type == keyboard.KEY_DOWN and e.name == TRIGGER_KEY:
            current_time = time.time()
            if current_time - last_s_press < DOUBLE_PRESS_THRESHOLD:
                # Use after() to schedule GUI update on main thread
                app.after(0, app.show_window)
                last_s_press = 0 # Reset to prevent triple-click triggering twice
            else:
                last_s_press = current_time

    print(f"App started. Double press '{TRIGGER_KEY}' to trigger popup.")
    keyboard.hook(on_key)
    
    try:
        app.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.unhook_all()

if __name__ == "__main__":
    run_app()
