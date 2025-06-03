"""
Main application entry point.
This module serves as the controller for the entire application, managing the main window
and coordinating between different views (login, signup, and main application).
"""

import os
from pathlib import Path
import customtkinter as ctk
from customtkinter import CTk, CTkFrame

# Import application views
from frontend.login import LoginView
from frontend.signup import SignupView
from frontend.index import MainAppUI

# Set the application appearance mode to dark
ctk.set_appearance_mode("dark")

class ApplicationController:
    """
    Main controller class that manages the application's main window and view transitions.
    
    This class is responsible for:
    - Initializing and configuring the main application window
    - Managing transitions between different views (login, signup, main app)
    - Handling the application's lifecycle
    """

    def __init__(self):
        """Initialize the application controller and setup the main window."""
        self.main_window = CTk()
        self.main_window.geometry("400x700")
        self.setup_main_window()

    def setup_main_window(self):
        """
        Configure the main application window settings.
        Sets up the window title, size, icon, and initial frame.
        """
        # Configure window properties
        self.main_window.title("Dobot")
        self.main_window.config(bg="#2E2E2E")
        self.main_window.resizable(False, False)

        # Set application icon
        icon_path = os.path.join(
            Path(__file__).resolve().parent,
            "frontend",
            "assets",
            "icons",
            "dob.ico"
        )
        self.main_window.iconbitmap(icon_path)

        # Create the authentication frame for login/signup views
        self.auth_frame = CTkFrame(
            self.main_window,
            fg_color="#2E2E2E",
            bg_color="white",
            width=300,
            height=300,
            corner_radius=0
        )
        self.auth_frame.pack(pady=50, fill="both", expand=True)

    def show_login(self):
        """
        Display the login view.
        Creates a new LoginView instance with callbacks for successful login
        and navigation to signup.
        """
        LoginView(
            self.main_window,
            self.auth_frame,
            on_login_success=self.open_main_app,
            on_go_to_signup=self.show_signup
        )

    def show_signup(self):
        """
        Display the signup view.
        Creates a new SignupView instance with a callback to return to login.
        """
        SignupView(
            self.main_window,
            self.auth_frame,
            on_go_to_login=self.show_login
        )

    def open_main_app(self, expiration_date=None):
        """
        Open the main application interface.
        
        Args:
            expiration_date (str, optional): The user's subscription expiration date.
                                            Defaults to None.
        """
        # Clean up authentication frame
        if hasattr(self, 'auth_frame') and self.auth_frame:
            self.auth_frame.destroy()
            self.auth_frame = None

        # Clear all existing widgets from the main window
        for widget in self.main_window.winfo_children():
            widget.destroy()

        # Initialize and open the main application UI
        app = MainAppUI(self.main_window, expiration_date=expiration_date)
        app.open()

    def run(self):
        """
        Start the application.
        Initializes the login view and begins the main event loop.
        """
        self.show_login()
        self.main_window.mainloop()


if __name__ == "__main__":
    # Create and run the application
    app = ApplicationController()
    app.run()