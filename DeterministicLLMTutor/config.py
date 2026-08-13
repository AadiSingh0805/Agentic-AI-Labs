import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_gemini_model():
    """
    Initializes and returns the Gemini model with temperature=0 and top_p=1
    to enforce deterministic, zero-variability outputs.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise ValueError(
            "GEMINI_API_KEY is missing or invalid in .env file. "
            "Please provide a valid Google Gemini API key."
        )

    genai.configure(api_key=GEMINI_API_KEY)

    # Use gemini-1.5-flash for speed and deterministic rephrasing
    generation_config = {
        "temperature": 0.0,
        "top_p": 1.0,
    }

    model = genai.GenerativeModel(
        model_name="gemini-3.5-flash",
        generation_config=generation_config
    )
    
    return model