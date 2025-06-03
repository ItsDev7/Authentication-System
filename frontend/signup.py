"""
Signup Module

This module handles the user registration interface and signup process.
It provides a graphical interface for users to create new accounts,
with features like password visibility toggle and social media links.

Dependencies:
    - customtkinter: For modern UI components
    - requests: For API communication
    - PIL: For image handling
    - python-dotenv: For environment variable management
"""

import os
from pathlib import Path
import requests
from PIL import Image
from tkinter import messagebox
from customtkinter import (
    CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkImage
)
from dotenv import load_dotenv
from frontend.utlis.tooltip import ToolTip

# Load environment variables
load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000/api')


class SignupView:
    """
    Signup View class that manages the registration interface and signup process.
    
    This class handles:
    - Signup form UI creation and management
    - User registration
    - Password visibility toggle
    - Form validation
    """

    def __init__(self, main, auth_frame, on_go_to_login):
        """
        Initialize the signup view.
        
        Args:
            main: The root CTk window
            auth_frame: The authentication frame
            on_go_to_login: Callback function to switch to login view
        """
        self.main = main
        self.auth_frame = auth_frame
        self.on_go_to_login = on_go_to_login
        self.setup_ui()

    def clear_frame(self):
        """Remove all widgets from the authentication frame."""
        for widget in self.auth_frame.winfo_children():
            widget.destroy()

    def setup_ui(self):
        """Build the complete signup interface."""
        self.clear_frame()
        self._create_title_section()
        self._create_signup_form()
        self._create_social_links()
        self._create_footer()
        self._create_error_label()

    def _create_title_section(self):
        """Create the title and decorative elements at the top of the signup form."""
        # Main title
        title = CTkLabel(
            self.auth_frame,
            text="D O B O T",
            font=("Arial Black", 28),
            text_color="#00CFFF"
        )
        title.pack(pady=(40, 10))

        # Decorative line
        line = CTkLabel(
            self.auth_frame,
            text="⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯◈⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
            text_color="#00CFFF",
            font=("Arial", 18)
        )
        line.pack(pady=5)

        # Page title
        title_page = CTkLabel(
            self.auth_frame,
            text="Sign up",
            text_color="white",
            font=("Arial Black", 18)
        )
        title_page.pack(pady=1)

    def _create_signup_form(self):
        """Create the main signup form with username and password fields."""
        # Username field
        self._create_username_field()
        
        # Password field
        self._create_password_field()
        
        # Create account button
        self._create_signup_button()
        
        # Login link
        self._create_login_link()

    def _create_username_field(self):
        """Create the username input field with its label."""
        username_frame = CTkFrame(self.auth_frame, fg_color="transparent")
        username_frame.pack(pady=(30, 10))

        username_label = CTkLabel(
            username_frame,
            text="Username:",
            text_color="white",
            font=("Arial", 14)
        )
        username_label.pack(side="left", padx=(0, 10))

        self.username_entry = CTkEntry(
            username_frame,
            text_color="white",
            fg_color="#1C1C1C",
            border_color="white",
            font=("", 14),
            width=200,
            corner_radius=5,
            border_width=1,
            height=35
        )
        self.username_entry.pack(side="left")
        self.username_entry.bind("<Key>", lambda e: self.username_entry.configure(border_color="white"))

    def _create_password_field(self):
        """Create the password input field with its label and visibility toggle."""
        password_frame = CTkFrame(self.auth_frame, fg_color="transparent")
        password_frame.pack(pady=(10, 10))

        password_label = CTkLabel(
            password_frame,
            text="Password:",
            text_color="white",
            font=("Arial", 14)
        )
        password_label.pack(side="left", padx=(50, 10))

        self.password_entry = CTkEntry(
            password_frame,
            text_color="white",
            fg_color="#1C1C1C",
            border_color="white",
            font=("", 14),
            width=200,
            corner_radius=5,
            border_width=1,
            height=35,
            show="*"
        )
        self.password_entry.pack(side="left")
        self.password_entry.bind("<Key>", lambda e: self.password_entry.configure(border_color="white"))

        # Password visibility toggle button
        self.eye_button = CTkButton(
            password_frame,
            text='👁',
            width=20,
            height=20,
            fg_color="#2E2E2E",
            hover_color="#1C1C1C",
            text_color="white",
            font=("", 18),
            corner_radius=15,
            command=self.toggle_password
        )
        self.eye_button.pack(side="left")

    def _create_signup_button(self):
        """Create the signup button."""
        create_frame = CTkFrame(self.auth_frame, fg_color="transparent")
        create_frame.pack(pady=20)

        create_btn = CTkButton(
            create_frame,
            text="➜",
            font=("", 20, "bold"),
            height=40,
            width=60,
            fg_color="#0085FF",
            cursor="hand2",
            corner_radius=15,
            command=self.sign_up
        )
        create_btn.pack(side="left", padx=10)

    def _create_login_link(self):
        """Create the login link section."""
        login_text_frame = CTkFrame(self.auth_frame, fg_color="transparent")
        login_text_frame.pack(pady=(10, 10))

        login_text = CTkLabel(
            login_text_frame,
            text="Do you already have an account? ",
            text_color="white",
            cursor="hand2",
            font=("", 12)
        )
        login_text.pack(side="left", padx=(0, 10))

        login_link = CTkLabel(
            login_text_frame,
            text="Log In",
            text_color="#0085FF",
            cursor="hand2",
            font=("", 12)
        )
        login_link.pack(side="left")

        # Hover effects for login link
        login_link.bind("<Enter>", lambda e: login_link.configure(text_color="#4169E1"))
        login_link.bind("<Leave>", lambda e: login_link.configure(text_color="#0085FF"))

        # Click handlers
        login_text.bind("<Button-1>", lambda e: self.go_to_login())
        login_link.bind("<Button-1>", lambda e: self.go_to_login())

    def _create_social_links(self):
        """Create social media links section."""
        icons_frame = CTkFrame(self.auth_frame, fg_color="transparent")
        icons_frame.pack(pady=20)

        # GitHub button
        github_path = os.path.join(Path(__file__).resolve().parent, "assets", "icons", "icon-github.png")
        github_icon = CTkImage(light_image=Image.open(github_path), size=(24, 24))
        github_btn = CTkButton(
            icons_frame,
            text="",
            image=github_icon,
            width=36
        )
        ToolTip(github_btn, "My GitHub")
        github_btn.pack(side="left", padx=10)

        # X (Twitter) button
        x_path = os.path.join(Path(__file__).resolve().parent, "assets", "icons", "icon-x.png")
        x_icon = CTkImage(light_image=Image.open(x_path), size=(24, 24))
        x_btn = CTkButton(
            icons_frame,
            text="",
            image=x_icon,
            width=36
        )
        ToolTip(x_btn, "X")
        x_btn.pack(side="left", padx=10)

        # Discord button
        discord_path = os.path.join(Path(__file__).resolve().parent, "assets", "icons", "icon-discord.png")
        discord_icon = CTkImage(light_image=Image.open(discord_path), size=(24, 24))
        discord_btn = CTkButton(
            icons_frame,
            text="",
            image=discord_icon,
            width=36
        )
        ToolTip(discord_btn, "Discord")
        discord_btn.pack(side="left", padx=10)

    def _create_footer(self):
        """Create the footer section with copyright and version information."""
        CTkLabel(
            self.auth_frame,
            text="© 2025 by @ItsDev",
            text_color="gray",
            font=("Arial", 10)
        ).pack(pady=(10, 0))
        
        CTkLabel(
            self.auth_frame,
            text="Version 1.0.2",
            text_color="gray",
            font=("Arial", 10)
        ).pack()

    def _create_error_label(self):
        """Create the error message label."""
        self.error_label = CTkLabel(
            self.auth_frame,
            text="",
            text_color="red",
            font=("Arial", 11),
            bg_color="transparent"
        )
        self.error_label.place(x=150, y=280)

    def toggle_password(self):
        """Toggle password visibility."""
        if self.password_entry.cget('show') == '':
            self.password_entry.configure(show='*')
            self.eye_button.configure(text='👁')
        else:
            self.password_entry.configure(show='')
            self.eye_button.configure(text='🔒')

    def sign_up(self):
        """Handle signup form submission and account creation."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Validate input
        if len(username) < 8:
            self.username_entry.configure(border_color="red")
            self.error_label.configure(text="Username must be at least 8 characters long.")
            return
        if len(password) < 8:
            self.password_entry.configure(border_color="red")
            self.error_label.configure(text="Password must be at least 8 characters long.")
            return

        # Prepare signup request
        url = f"{API_BASE_URL}/signup/"
        data = {
            "username": username,
            "password": password
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                self._handle_successful_signup()
            elif response.status_code == 409:
                self._handle_username_taken()
            else:
                self._handle_signup_error()
        except requests.exceptions.RequestException as err:
            self.error_label.configure(text=f"Error: {err}")

    def _handle_successful_signup(self):
        """Handle successful account creation."""
        self.error_label.configure(text="")
        self.username_entry.configure(border_color="white")
        self.password_entry.configure(border_color="white")
        messagebox.showinfo(
            "Success",
            "Account created successfully.\nPlease activate your account using a license key."
        )
        self.go_to_login()

    def _handle_username_taken(self):
        """Handle case where username is already taken."""
        self.username_entry.configure(border_color="red")
        self.error_label.configure(text="This username is already in use.")

    def _handle_signup_error(self):
        """Handle general signup errors."""
        self.error_label.configure(text="Failed to create account.")

    def go_to_login(self):
        """Navigate to the login view."""
        self.on_go_to_login()