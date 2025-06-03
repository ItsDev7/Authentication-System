"""
Login Module

This module handles the login interface and authentication process.
It provides a graphical interface for users to log in to their accounts,
with features like remember me, password visibility toggle, and social media links.

Dependencies:
    - customtkinter: For modern UI components
    - requests: For API communication
    - PIL: For image handling
    - python-dotenv: For environment variable management
"""

import os
from pathlib import Path
import json
import requests
from PIL import Image
import tkinter.messagebox as messagebox
from customtkinter import (
    CTkFrame, CTkLabel, CTkEntry, CTkButton,
    CTkCheckBox, CTkImage, CTkToplevel
)
from dotenv import load_dotenv
from frontend.license import LicenseDialog
from frontend.index import MainAppUI
from frontend.utlis.tooltip import ToolTip

# Load environment variables
load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000/api')


class LoginView:
    """
    Login View class that manages the login interface and authentication process.
    
    This class handles:
    - Login form UI creation and management
    - User authentication
    - Remember me functionality
    - Password visibility toggle
    """

    def __init__(self, main, auth_frame, on_login_success, on_go_to_signup):
        """
        Initialize the login view.
        
        Args:
            main: The root CTk window
            auth_frame: The authentication frame
            on_login_success: Callback function for successful login
            on_go_to_signup: Callback function to switch to signup view
        """
        self.main = main
        self.auth_frame = auth_frame
        self.on_login_success = on_login_success
        self.on_go_to_signup = on_go_to_signup
        self.remember_me_file = "remember_me.json"
        self.setup_ui()
        self._load_remember_me_data()

    def clear_frame(self):
        """Remove all widgets from the authentication frame."""
        for widget in self.auth_frame.winfo_children():
            widget.destroy()

    def setup_ui(self):
        """Build the complete login interface."""
        self.clear_frame()
        self._create_title_section()
        self._create_login_form()
        self._create_social_links()
        self._create_footer()
        self._create_error_label()

    def _create_title_section(self):
        """Create the title and decorative elements at the top of the login form."""
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
            text="Log in",
            text_color="white",
            font=("Arial Black", 18)
        )
        title_page.pack(pady=1)

    def _create_login_form(self):
        """Create the main login form with username and password fields."""
        # Username field
        self._create_username_field()
        
        # Password field
        self._create_password_field()
        
        # Remember me and forgot password section
        self._create_remember_me_section()
        
        # Login button
        self._create_login_button()
        
        # Sign up link
        self._create_signup_link()

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

    def _create_remember_me_section(self):
        """Create the remember me checkbox and forgot password link."""
        bottom_frame = CTkFrame(self.auth_frame, fg_color="transparent", height=40)
        bottom_frame.pack(fill="x", pady=(10, 10), padx=20)

        # Remember me checkbox
        self.remember_check = CTkCheckBox(
            bottom_frame,
            text="Remember Me",
            text_color="white",
            font=("Arial", 12),
            onvalue="yes",
            offvalue="no",
            border_color="white",
            checkbox_height=15,
            checkbox_width=15,
            corner_radius=5,
            border_width=1
        )
        self.remember_check.place(x=100, y=3)

        # Forgot password button
        forgot_btn = CTkButton(
            bottom_frame,
            text="Forgot Password?",
            text_color="#1E90FF",
            font=("Arial", 12),
            fg_color="transparent",
            hover_color="#2E2E2E",
            cursor="hand2",
            width=120,
            anchor="e",
            command=lambda: print("Open reset password page")
        )
        forgot_btn.place(relx=1.0, x=-5, y=2, anchor="ne")

        # Hover effects for forgot password button
        forgot_btn.bind("<Enter>", lambda e: forgot_btn.configure(text_color="#4169E1"))
        forgot_btn.bind("<Leave>", lambda e: forgot_btn.configure(text_color="#1E90FF"))

    def _create_login_button(self):
        """Create the login button."""
        login_frame = CTkFrame(self.auth_frame, fg_color="transparent")
        login_frame.pack(pady=20)

        login_btn = CTkButton(
            login_frame,
            text="➜",
            font=("", 20, "bold"),
            height=40,
            width=60,
            fg_color="#0085FF",
            cursor="hand2",
            corner_radius=15,
            command=self.login_action
        )
        login_btn.pack(side="left", padx=10)

    def _create_signup_link(self):
        """Create the sign up link section."""
        signup_text_frame = CTkFrame(self.auth_frame, fg_color="transparent")
        signup_text_frame.pack(pady=(10, 10))

        signup_text = CTkLabel(
            signup_text_frame,
            text="Don't have an account? ",
            text_color="white",
            cursor="hand2",
            font=("", 12)
        )
        signup_text.pack(side="left", padx=(0, 10))

        signup_link = CTkLabel(
            signup_text_frame,
            text="Sign Up",
            text_color="#0085FF",
            cursor="hand2",
            font=("", 12)
        )
        signup_link.pack(side="left")

        # Hover effects for sign up link
        signup_link.bind("<Enter>", lambda e: signup_link.configure(text_color="#4169E1"))
        signup_link.bind("<Leave>", lambda e: signup_link.configure(text_color="#0085FF"))

        # Click handlers
        signup_text.bind("<Button-1>", lambda e: self.on_go_to_signup())
        signup_link.bind("<Button-1>", lambda e: self.on_go_to_signup())

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

    def login_action(self):
        """Handle login form submission and authentication."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Validate input
        if not username:
            self.error_label.configure(text="Please fill Username")
            self.username_entry.configure(border_color="red")
            return
        if not password:
            self.error_label.configure(text="Please fill Password")
            self.password_entry.configure(border_color="red")
            return

        # Prepare login request
        url = f"{API_BASE_URL}/login/"
        data = {
            "username": username,
            "password": password
        }

        try:
            response = requests.post(url, json=data)
            response_data = response.json()

            if response.status_code == 200:
                # Handle successful login
                print("DEBUG: Login response_data:", response_data)
                expiration_date = response_data.get("expiration_date")
                
                # Handle remember me
                if self.remember_check.get() == "yes":
                    self._save_remember_me_data(username)
                else:
                    self._clear_remember_me_data()
                    
                MainAppUI(self.main, expiration_date=expiration_date).open()
                
            elif response.status_code == 403:
                self._handle_activation_required(response_data)
            else:
                self._handle_login_error(response_data)

        except requests.exceptions.RequestException as err:
            self.error_label.configure(text="Network error.")

    def _handle_activation_required(self, response_data):
        """Handle case where account activation is required."""
        detail_msg = response_data.get("detail", "")
        if "activation code" in detail_msg.lower():
            self.error_label.configure(text="")
            self.username_entry.configure(border_color="white")
            self.password_entry.configure(border_color="white")
            
            user_id = response_data.get("user_id")
            if user_id:
                LicenseDialog(self.main, self.username_entry.get(), user_id)
            else:
                messagebox.showerror("Login Error", "Could not retrieve user ID for activation.")
        else:
            self._handle_login_error(response_data)

    def _handle_login_error(self, response_data):
        """Handle login error response."""
        self.error_label.configure(text=response_data.get("detail", "Login failed"))
        self.username_entry.configure(border_color="red")
        self.password_entry.configure(border_color="red")

    def _save_remember_me_data(self, username):
        """Save remember me data to file."""
        data = {"username": username, "remember_me": True}
        with open(self.remember_me_file, 'w') as f:
            json.dump(data, f)

    def _load_remember_me_data(self):
        """Load remember me data from file."""
        if os.path.exists(self.remember_me_file):
            try:
                with open(self.remember_me_file, 'r') as f:
                    data = json.load(f)
                    if data.get("remember_me"):
                        self.username_entry.insert(0, data.get("username", ""))
                        self.remember_check.select()
            except (json.JSONDecodeError, FileNotFoundError):
                self._clear_remember_me_data()

    def _clear_remember_me_data(self):
        """Clear remember me data file."""
        if os.path.exists(self.remember_me_file):
            os.remove(self.remember_me_file)

    def go_to_signup(self):
        """Navigate to the signup view."""
        self.on_go_to_signup()