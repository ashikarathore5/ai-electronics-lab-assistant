import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API Key missing! Please check your .env file.")
genai.configure(api_key=API_KEY)

# Define the Master System Instruction
SYSTEM_INSTRUCTION = """
You are an expert Electronic and Communication Engineering (ECE) Lab Assistant. 
Your task is to analyze the provided image of a circuit (breadboard, PCB, or schematic) and provide a highly structured analysis.

You must output your response in exactly three distinct sections using these specific headers:
1. ### 🔍 Component Identification
   List all detected components (e.g., Resistors, Capacitors, LEDs, ICs, Transistors, Microcontrollers). If visible, try to estimate values (e.g., resistor color bands, capacitor markings).
   
2. ### ⚡ Circuit Analysis & Theory
   Explain what this circuit does (e.g., "It's an astable multivibrator using a 555 timer"). Explain the underlying ECE core theory and formulas briefly (e.g., Ohm's Law, time constant $\\tau = R \\times C$).
   
3. ### ⚠️ Common Mistakes & Troubleshooting
   Point out potential flaws visible in the image (e.g., "The LED is missing a current-limiting resistor", "The polarized capacitor might be reversed", "Check for loose jumper wires"). If the circuit looks perfect, provide 2-3 standard troubleshooting steps a student should take if it doesn't power up.

Be concise, academic, yet encouraging. Use LaTeX formatting for any equations.
"""

def analyze_circuit_image(image: Image.Image) -> str:
    """Passes the image to Gemini-2.5-Flash along with our system instructions."""
    # Using gemini-2.5-flash as it is highly efficient and fast for multimodal tasks
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_INSTRUCTION
    )
    
    # Prompting the model to execute based on its system instructions
    response = model.generate_content([
        "Analyze this circuit image thoroughly according to your system instructions.", 
        image
    ])
    
    return response.text