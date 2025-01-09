import customtkinter as ctk
from config import *

class HabitRecommenderGUI(ctk.CTk):
    """Main GUI class that inherits from CTk (CustomTkinter's main window class)"""
    
    def __init__(self, recommend_callback):
        """
        Initialize the GUI window
        Args:
            recommend_callback: Function to call when recommendation is requested
        """
        super().__init__()  # Initialize parent class
        
        self.recommend_callback = recommend_callback  # Store callback function
        
        # Set up basic window properties
        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)
        
        # Create different font styles for various UI elements
        self.fonts = {
            "title": ctk.CTkFont(**FONT_CONFIG["title"]),
            "body": ctk.CTkFont(**FONT_CONFIG["body"]),
            "loading": ctk.CTkFont(**FONT_CONFIG["loading"])
        }
        
        # Configure window grid layout - make it expandable
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main container frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=PADDING["default"], 
                           pady=PADDING["default"], sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self._create_widgets()  # Set up all UI elements
    
    def _create_widgets(self):
        """Create and configure all UI elements"""
        
        # Create title label at top of window
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text=TEXTS["title"],
            font=self.fonts["title"]
        )
        self.title_label.grid(row=0, column=0, padx=PADDING["title"][0], 
                            pady=PADDING["title"][1])
        
        # Create text input box for journal entries
        self.journal_input = ctk.CTkTextbox(
            self.main_frame,
            height=200,
            font=self.fonts["body"]
        )
        self.journal_input.grid(row=1, column=0, padx=PADDING["input"][0], 
                              pady=PADDING["input"][1], sticky="ew")
        
        # Create recommendation button
        self.recommend_button = ctk.CTkButton(
            self.main_frame,
            text=TEXTS["button"],
            command=self._on_recommend_click  # Connect to click handler
        )
        self.recommend_button.grid(row=3, column=0, padx=PADDING["button"][0], 
                                 pady=PADDING["button"][1])
        
        # Create loading indicator (hidden by default)
        self.loading_label = ctk.CTkLabel(
            self.main_frame,
            text=TEXTS["loading"],
            text_color="gray",
            font=self.fonts["loading"]
        )
        self.loading_label.grid(row=4, column=0, padx=PADDING["loading"][0], 
                              pady=PADDING["loading"][1])
        self.loading_label.grid_remove()  # Hide initially
        
        # Create label for displaying recommendations
        self.recommendation_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            wraplength=500,  # Enable text wrapping
            font=self.fonts["body"]
        )
        self.recommendation_label.grid(row=5, column=0, padx=PADDING["default"], 
                                     pady=PADDING["default"])
        
        # Create character counter label
        self.char_counter = ctk.CTkLabel(
            self.main_frame,
            text="0/500 characters",
            font=self.fonts["loading"],
            text_color="gray"
        )
        self.char_counter.grid(row=2, column=0, padx=PADDING["default"], 
                             pady=(0, 10), sticky="e")
        
        # Add new binding for key press (before character is inserted)
        self.journal_input.bind("<Key>", self._check_char_limit)
        # Keep existing binding for after key release
        self.journal_input.bind("<KeyRelease>", self._update_char_count)

    def _update_char_count(self, event=None):
        """
        Update character counter when text changes
        Args:
            event: Keyboard event (optional)
        """
        current_text = self.journal_input.get("1.0", "end-1c")  # Get current text
        char_count = len(current_text)
        max_chars = 500
        
        # Only delete excess characters if we're over the limit
        if char_count > max_chars:
            # Keep first 500 characters, delete the rest
            excess = char_count - max_chars
            end_pos = "end-" + str(excess) + "c"
            self.journal_input.delete(end_pos, "end")
            char_count = max_chars
        
        # Update counter display
        self.char_counter.configure(
            text=f"{char_count}/{max_chars} characters",
            text_color="gray" if char_count < max_chars else "red"
        )

    def _on_recommend_click(self):
        """Handle recommendation button click"""
        journal_entry = self.journal_input.get("1.0", "end-1c")  # Get text input
        
        # Validate input is not empty
        if not journal_entry.strip():
            self.recommendation_label.configure(text=TEXTS["error_empty"])
            return
        
        # Show loading state
        self.loading_label.grid()
        self.recommend_button.configure(state="disabled")
        self.update()  # Force GUI update
        
        try:
            # Call recommendation callback and display result
            habit = self.recommend_callback(journal_entry)
            self.recommendation_label.configure(text=habit)
        except Exception as e:
            # Handle and display errors
            self.recommendation_label.configure(text=f"Error: {str(e)}")
        finally:
            # Reset UI state
            self.loading_label.grid_remove()
            self.recommend_button.configure(state="normal") 

    def _check_char_limit(self, event):
        """
        Prevent typing beyond 500 characters
        Args:
            event: Keyboard event
        """
        current_text = self.journal_input.get("1.0", "end-1c")
        
        # Allow special keys (backspace, delete, arrows, etc.)
        if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down'):
            return
        
        # If at 500 characters, prevent new character input
        if len(current_text) >= 500:
            return "break"  # This prevents the character from being inserted 