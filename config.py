import customtkinter as ctk

# Window settings
WINDOW_TITLE = "Habit Recommender"
WINDOW_SIZE = "800x600"

# Font configurations
FONT_CONFIG = {
    "title": {
        "size": 24,
        "weight": "bold"
    },
    "body": {
        "size": 14
    },
    "loading": {
        "size": 12,
        "slant": "italic"
    }
}

# Layout settings
PADDING = {
    "default": 20,
    "title": (20, 10),
    "input": (0, 20),
    "button": (0, 20),
    "loading": (0, 5),
}

# Text content
TEXTS = {
    "title": "Daily Journal",
    "button": "Get Habit Recommendation",
    "loading": "Getting recommendation...",
    "error_empty": "Please enter a journal entry!",
}

# OpenAI settings
OPENAI_CONFIG = {
    "model": "gpt-4",
    "max_tokens": 50,
    "temperature": 0.7,
}

# Prompt template
PROMPT_TEMPLATE = """Given the following journal entry, recommend one specific, actionable habit that would be most helpful for the person.
The habit should be practical and directly address the main concern or theme in the journal entry.

Journal entry: {journal_entry}

Return only the recommended habit without any additional explanation."""

SYSTEM_PROMPT = "You are a habit recommendation expert. Keep suggestions practical and positive. Respond only with the recommended habit." 