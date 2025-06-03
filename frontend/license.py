"""
License Activation Module

This module handles the license activation process for user accounts.
It provides a graphical interface for users to enter and validate their license keys,
and communicates with the backend API for license validation and activation.

Dependencies:
    - customtkinter: For modern UI components
    - requests: For API communication
    - python-dotenv: For environment variable management
"""

import customtkinter as ctk
from tkinter import messagebox
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from pathlib import Path

# Load environment variables
load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')


class LicenseDialog:
    """
    A dialog window for license activation.
    
    This class creates and manages a modal window where users can enter
    their license key to activate their account. It handles both the UI
    and the communication with the backend API.
    """

    def __init__(self, main, username, user_id):
        """
        Initialize the license dialog window.
        
        Args:
            main: The parent window
            username: The username of the current user
            user_id: The ID of the current user
        """
        print("LicenseDialog is being initialized...")
        self.main = main
        self.username = username
        self.user_id = user_id
        self.build_ui()

    def build_ui(self):
        """
        Build the license activation dialog UI.
        
        Creates and configures all UI elements including:
        - Main window
        - Title and info labels
        - License key entry field
        - Activation button
        """
        # Create and configure the main window
        self.license_window = ctk.CTkToplevel(self.main)
        self.license_window.title("🔑 Activate Your Account")
        self.license_window.config(bg="#2E2E2E")
        self.license_window.geometry("400x240")
        self.license_window.resizable(False, False)
        
        # Set window icon
        icon_path = os.path.join(Path(__file__).resolve().parent, "assets", "icons", "dob.ico")
        self.license_window.iconbitmap(icon_path)
        
        # Center the window and make it modal
        self.center_window(self.license_window, 400, 240)
        self.license_window.transient(self.main)
        self.license_window.grab_set()

        # Create title label
        label_title = ctk.CTkLabel(
            self.license_window,
            text="Account Activation",
            fg_color="#2E2E2E",
            font=ctk.CTkFont("Segoe UI", 16, "bold"),
            text_color="#00ADB5"
        )
        label_title.pack(pady=(20, 5))

        # Create info label
        label_info = ctk.CTkLabel(
            self.license_window,
            text="Your account is not activated.\nPlease enter your activation key below:",
            fg_color="#2E2E2E",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color="white"
        )
        label_info.pack(pady=(0, 10))

        # Create entry frame and license key input
        self._create_license_entry()

        # Create activation button
        self._create_activation_button()

    def _create_license_entry(self):
        """
        Create the license key entry field with its container frame.
        """
        entry_frame = ctk.CTkFrame(self.license_window, fg_color="#2E2E2E")
        entry_frame.pack(pady=(0, 10))

        # Add key icon
        icon_label = ctk.CTkLabel(
            entry_frame,
            text="🔑",
            font=ctk.CTkFont(size=16),
            text_color="white"
        )
        icon_label.pack(side="left", padx=(0, 5))

        # Create entry field
        self.entry_license = ctk.CTkEntry(
            entry_frame,
            width=200,
            font=ctk.CTkFont(size=12),
            fg_color="#1C1C1C",
            text_color="white",
            corner_radius=5,
            border_width=1,
            justify="center",
            placeholder_text="Enter your license key"
        )
        self.entry_license.pack(side="left")

    def _create_activation_button(self):
        """
        Create the activation button with its styling and command.
        """
        self.btn_activate = ctk.CTkButton(
            self.license_window,
            text="Activate Now",
            font=ctk.CTkFont("Segoe UI", 11, "bold"),
            fg_color="#44bd32",
            hover_color="#4cd137",
            text_color="white",
            cursor="hand2",
            corner_radius=1,
            command=self.activate_account
        )
        self.btn_activate.pack(pady=(5, 15))

    def center_window(self, window, width, height):
        """
        Center the window on the screen.
        
        Args:
            window: The window to center
            width: Window width
            height: Window height
        """
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def activate_account(self):
        """
        Handle the license activation process.
        
        This method:
        1. Validates the license key format
        2. Sends validation request to the API
        3. If valid, sends activation request
        4. Handles the response and shows appropriate messages
        """
        license_key = self.entry_license.get().strip()

        if not license_key:
            messagebox.showwarning("Missing Key", "Please enter an activation key.")
            return

        # Validate license key
        if not self._validate_license(license_key):
            return

        # Activate license
        self._activate_license(license_key)

    def _validate_license(self, license_key):
        """
        Validate the license key with the backend API.
        
        Args:
            license_key: The license key to validate
            
        Returns:
            bool: True if validation successful, False otherwise
        """
        validate_url = f"{API_BASE_URL}/license/validate/{license_key}"
        try:
            validate_response = requests.post(validate_url)
            validate_result = validate_response.json()
            
            if validate_response.status_code != 200 or not validate_result.get("is_valid"):
                messagebox.showerror(
                    "Validation Failed",
                    validate_result.get("message", "Invalid or expired key.")
                )
                return False

            # Show expiration date if available
            expires_at = validate_result.get("expires_at")
            if expires_at and expires_at != "None":
                try:
                    dt = datetime.fromisoformat(expires_at)
                    expires_str = dt.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    expires_str = expires_at
                messagebox.showinfo(
                    "License Valid",
                    f"Your license is valid.\nYour account will be activated until: {expires_str}"
                )
            return True
            
        except Exception as e:
            messagebox.showerror("Validation Error", f"Could not validate license: {e}")
            return False

    def _activate_license(self, license_key):
        """
        Activate the license key for the user.
        
        Args:
            license_key: The license key to activate
        """
        activate_url = f"{API_BASE_URL}/license/activate/{license_key}?user_id={self.user_id}"
        try:
            activate_response = requests.post(activate_url)
            activate_result = activate_response.json()
            print("DEBUG activate_result:", activate_result)
            
            if activate_response.status_code == 200:
                self._handle_successful_activation(activate_result)
            else:
                messagebox.showerror(
                    "Activation Failed",
                    activate_result.get("detail", "An error occurred during activation.")
                )
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Failed to connect to server:\n{e}")
        except Exception as e:
            messagebox.showerror("An Error Occurred", f"An unexpected error occurred:\n{e}")

    def _handle_successful_activation(self, activate_result):
        """
        Handle successful license activation.
        
        Args:
            activate_result: The API response containing activation details
        """
        expires_at = activate_result.get("expires_at")
        msg = activate_result.get("message", "Account activated successfully!")
        
        if expires_at:
            try:
                dt = datetime.fromisoformat(expires_at)
                expires_str = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                expires_str = str(expires_at)
            msg += f"\nExpires at: {expires_str}"
            
        messagebox.showinfo("Success", msg)
        self.license_window.destroy()
