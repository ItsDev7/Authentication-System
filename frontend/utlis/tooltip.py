"""
Tooltip Module

This module provides a custom tooltip implementation for tkinter widgets.
It creates a floating tooltip that appears when hovering over a widget
and disappears when the mouse leaves the widget.

Dependencies:
    - tkinter: For GUI components and window management
"""

import tkinter as tk


class ToolTip:
    """
    A custom tooltip class that creates a floating tooltip for tkinter widgets.
    
    This class handles:
    - Tooltip creation and positioning
    - Show/hide behavior on mouse hover
    - Custom styling of the tooltip window
    
    Attributes:
        widget: The widget to attach the tooltip to
        text: The text to display in the tooltip
        tipwindow: The tooltip window instance
    """

    def __init__(self, widget, text):
        """
        Initialize the tooltip.
        
        Args:
            widget: The tkinter widget to attach the tooltip to
            text: The text to display in the tooltip
        """
        self.widget = widget
        self.text = text
        self.tipwindow = None
        
        # Bind mouse events to show/hide tooltip
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        """
        Display the tooltip window.
        
        Creates a new tooltip window if one doesn't exist and the tooltip text
        is not empty. Positions the tooltip near the widget.
        
        Args:
            event: The event that triggered the tooltip (optional)
        """
        # Don't show if tooltip already exists or text is empty
        if self.tipwindow or not self.text:
            return
            
        # Calculate tooltip position
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20

        # Create tooltip window
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Remove window decorations
        tw.wm_geometry(f"+{x}+{y}")  # Position the tooltip

        # Create and style the tooltip label
        label = tk.Label(
            tw,
            text=self.text,
            background="#333",  # Dark background
            foreground="white",  # White text
            relief="solid",  # Solid border
            borderwidth=1,
            font=("Arial", 10)
        )
        label.pack(ipadx=5, ipady=3)  # Add padding

    def hide_tip(self, event=None):
        """
        Hide the tooltip window.
        
        Destroys the tooltip window if it exists.
        
        Args:
            event: The event that triggered the hide action (optional)
        """
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
