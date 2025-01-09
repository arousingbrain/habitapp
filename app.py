from openai import OpenAI
from dotenv import load_dotenv
import os
from gui import HabitRecommenderGUI
from config import OPENAI_CONFIG, PROMPT_TEMPLATE, SYSTEM_PROMPT

class HabitRecommender:
    """Main class that handles habit recommendations based on journal entries"""
    
    def __init__(self):
        """Constructor method - initializes the application"""
        load_dotenv()  # Load environment variables from .env file
        # Create OpenAI client using API key stored in environment variables
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        # Create GUI instance and connect it to the recommend_habit method
        self.gui = HabitRecommenderGUI(recommend_callback=self.recommend_habit)
    
    def recommend_habit(self, journal_entry):
        """
        Method that sends journal entry to OpenAI API and gets habit recommendations
        Args:
            journal_entry (str): User's journal entry text
        Returns:
            str: AI-generated habit recommendation
        """
        try:
            # Make API call to OpenAI with the journal entry
            response = self.client.chat.completions.create(
                model=OPENAI_CONFIG["model"],  # AI model to use (e.g., GPT-4)
                messages=[
                    # System prompt defines how AI should behave
                    {"role": "system", "content": SYSTEM_PROMPT},
                    # User prompt contains the journal entry in a formatted template
                    {"role": "user", "content": PROMPT_TEMPLATE.format(
                        journal_entry=journal_entry
                    )}
                ],
                max_tokens=OPENAI_CONFIG["max_tokens"],  # Maximum length of response
                temperature=OPENAI_CONFIG["temperature"]  # Controls randomness of response
            )
            # Extract and return just the AI's message content
            return response.choices[0].message.content.strip()
        except Exception as e:
            # If any error occurs, raise it with additional context
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def run(self):
        """Starts the GUI application"""
        self.gui.mainloop()  # Start the main event loop of the GUI

# This block only runs if this file is run directly (not imported)
if __name__ == "__main__":
    app = HabitRecommender()  # Create instance of HabitRecommender
    app.run()  # Start the application 