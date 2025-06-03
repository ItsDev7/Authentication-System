"""
Main Application UI Module

This module contains the MainAppUI class which handles the main application interface,
including the countdown timer and basic UI elements. It uses customtkinter for
modern-looking UI components.
"""

from customtkinter import CTkFrame, CTkLabel
from datetime import datetime


class MainAppUI:
    """
    Main Application UI class that manages the primary interface of the application.
    
    This class handles:
    - Main window setup and configuration
    - Base frame creation
    - Countdown timer display
    - UI element management
    """

    def __init__(self, main, expiration_date=None):
        """
        Initialize the MainAppUI with the root window and optional expiration date.
        
        Args:
            main: The root window instance
            expiration_date (str, optional): ISO format date string for countdown timer
        """
        print("DEBUG: MainAppUI initialized with expiration_date:", expiration_date)
        self.main = main
        self.expiration_date = expiration_date
        self.main.geometry("750x650")
        self.countdown_label = None
        
        # Initialize UI components
        self.clear_main()
        self.build_base_frame()
        self.setup_hello_and_timer()

    def clear_main(self):
        """
        Remove all widgets from the main window.
        Used when resetting or updating the UI.
        """
        for widget in self.main.winfo_children():
            widget.destroy()

    def build_base_frame(self):
        """
        Create the main container frame for the application.
        
        Creates a CTkFrame as the main container with a dark background
        and configures the grid layout for proper widget placement.
        """
        self.main_app_frame = CTkFrame(
            self.main,
            fg_color="#2E2E2E",
            bg_color="white",
            corner_radius=0
        )
        self.main_app_frame.grid(row=0, column=0, sticky="nsew")
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

    def setup_hello_and_timer(self):
        """
        Set up the greeting label and countdown timer display.
        
        Creates and positions the 'Hello' label and countdown timer
        in the main application frame.
        """
        print("DEBUG: setup_hello_and_timer called, expiration_date:", self.expiration_date)
        
        # Create and position the greeting label
        hello_label = CTkLabel(
            self.main_app_frame,
            text="Hello",
            font=("Arial", 22),
            text_color="white"
        )
        hello_label.place(relx=0.5, rely=0.1, anchor="center")
        
        # Create and position the countdown label
        self.countdown_label = CTkLabel(
            self.main_app_frame,
            text="",
            font=("Arial", 16),
            text_color="#FF5555"
        )
        self.countdown_label.place(relx=0.5, rely=0.2, anchor="center")
        
        print("DEBUG: Hello label and countdown label created")
        if self.expiration_date:
            self.update_countdown()

    def update_countdown(self):
        """
        Update the countdown timer display.
        
        Calculates the time remaining until expiration and updates
        the countdown label. Recursively calls itself every second
        to keep the display current.
        """
        try:
            expire_dt = datetime.fromisoformat(self.expiration_date)
            now = datetime.now()
            delta = expire_dt - now
            
            if delta.total_seconds() > 0:
                days = delta.days
                hours, rem = divmod(delta.seconds, 3600)
                minutes, seconds = divmod(rem, 60)
                countdown_str = f"Time left: {days}d {hours}h {minutes}m {seconds}s"
            else:
                countdown_str = "Expired!"
        except Exception:
            countdown_str = "Unknown expiration"
            
        try:
            self.countdown_label.configure(text=countdown_str)
        except Exception:
            return
        
        # Schedule next update
        self.main.after(1000, self.update_countdown)

    def create_ui(self):
        """
        Create the main UI components.
        Currently just sets up the hello message and timer.
        """
        self.setup_hello_and_timer()

    def open(self):
        """
        Entry method to open the main application UI.
        
        Clears the main window, rebuilds the base frame,
        and initializes the UI components.
        """
        self.clear_main()
        self.build_base_frame()
        self.create_ui()